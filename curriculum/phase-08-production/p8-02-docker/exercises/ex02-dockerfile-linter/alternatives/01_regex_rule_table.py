import re
from collections.abc import Callable

_INST_RE = re.compile(r"^\s*([A-Za-z]+)(?:\s+(.*))?$")
_SECRET_ENV_RE = re.compile(r"\b[A-Za-z0-9_]*(?:KEY|TOKEN|SECRET)[A-Za-z0-9_]*\b", re.I)


def parse_dockerfile(text: str) -> list[tuple[str, str]]:
    """Parse a Dockerfile using line-continuation folding and a regex matcher."""
    cleaned_lines = [
        raw.strip() for raw in text.splitlines() if raw.strip() and not raw.strip().startswith("#")
    ]
    joined = re.sub(r"\s*\\\n\s*", " ", "\n".join(cleaned_lines))
    rows: list[tuple[str, str]] = []
    for line in joined.splitlines():
        match = _INST_RE.match(line.strip())
        if match:
            inst, args = match.groups()
            rows.append((inst.upper(), (args or "").strip()))
    return rows


def _unpinned_base(rows: list[tuple[str, str]]) -> bool:
    for inst, args in rows:
        if inst == "FROM" and args:
            img = args.split()[0]
            if ":" not in img or img.lower().endswith(":latest"):
                return True
    return False


def _copy_before_install(rows: list[tuple[str, str]]) -> bool:
    copy_pos = [
        i
        for i, (inst, args) in enumerate(rows)
        if inst == "COPY" and " ".join(args.split()) == ". ."
    ]
    pip_pos = [
        i
        for i, (inst, args) in enumerate(rows)
        if inst == "RUN" and "pip install" in " ".join(args.lower().split())
    ]
    return bool(copy_pos and pip_pos and copy_pos[0] < pip_pos[0])


def _secret_in_image(rows: list[tuple[str, str]]) -> bool:
    for inst, args in rows:
        if inst in ("COPY", "ADD") and re.search(r"(?:^|\s|/)\.env(?:\s|$)", args):
            return True
        if inst == "ENV" and args:
            key_part = args.split("=", 1)[0] if "=" in args else args.split()[0]
            env_hits = any(
                _SECRET_ENV_RE.search(t.split("=", 1)[0]) for t in args.split() if "=" in t
            )
            if _SECRET_ENV_RE.search(key_part) or env_hits:
                return True
    return False


def _localhost_cmd(rows: list[tuple[str, str]]) -> bool:
    return any(inst == "CMD" and re.search(r"127\.0\.0\.1|localhost", args) for inst, args in rows)


RULES: list[tuple[str, Callable[[list[tuple[str, str]]], bool]]] = [
    ("unpinned-base", _unpinned_base),
    ("copy-before-install", _copy_before_install),
    ("secret-in-image", _secret_in_image),
    ("localhost-cmd", _localhost_cmd),
]


def lint(text: str) -> list[str]:
    """Evaluate all declarative lint rules against the parsed Dockerfile."""
    rows = parse_dockerfile(text)
    return [code for code, check in RULES if check(rows)]
