def parse_dockerfile(text: str) -> list[tuple[str, str]]:
    """Parse a Dockerfile into uppercase (INSTRUCTION, args) tuples."""
    instructions: list[tuple[str, str]] = []
    pending = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("\\"):
            pending += line[:-1].rstrip() + " "
            continue
        full = (pending + line).strip()
        pending = ""
        parts = full.split(None, 1)
        inst = parts[0].upper()
        args = parts[1].strip() if len(parts) > 1 else ""
        instructions.append((inst, args))
    if pending.strip():
        parts = pending.strip().split(None, 1)
        instructions.append((parts[0].upper(), parts[1].strip() if len(parts) > 1 else ""))
    return instructions


def _has_unpinned_base(rows: list[tuple[str, str]]) -> bool:
    for inst, args in rows:
        if inst == "FROM" and args:
            image = args.split()[0]
            if ":" not in image or image.split(":")[-1].lower() == "latest":
                return True
    return False


def _has_copy_before_install(rows: list[tuple[str, str]]) -> bool:
    copy_all_idx = next(
        (
            i
            for i, (inst, args) in enumerate(rows)
            if inst == "COPY" and " ".join(args.split()) == ". ."
        ),
        None,
    )
    pip_idx = next(
        (
            i
            for i, (inst, args) in enumerate(rows)
            if inst == "RUN" and "pip install" in " ".join(args.lower().split())
        ),
        None,
    )
    return copy_all_idx is not None and pip_idx is not None and copy_all_idx < pip_idx


def _has_secret_in_image(rows: list[tuple[str, str]]) -> bool:
    secret_words = ("KEY", "TOKEN", "SECRET")
    for inst, args in rows:
        if inst in ("COPY", "ADD"):
            tokens = args.split()
            if any(tok == ".env" or tok.endswith("/.env") for tok in tokens):
                return True
        if inst == "ENV" and args:
            for token in args.split():
                name = token.split("=", 1)[0].upper()
                if any(word in name for word in secret_words):
                    return True
                if "=" not in args:
                    break
    return False


def _has_localhost_cmd(rows: list[tuple[str, str]]) -> bool:
    return any(
        inst == "CMD" and ("127.0.0.1" in args or "localhost" in args)
        for inst, args in rows
    )


def lint(text: str) -> list[str]:
    """Return Dockerfile lint warning codes in fixed order."""
    rows = parse_dockerfile(text)
    codes: list[str] = []
    if _has_unpinned_base(rows):
        codes.append("unpinned-base")
    if _has_copy_before_install(rows):
        codes.append("copy-before-install")
    if _has_secret_in_image(rows):
        codes.append("secret-in-image")
    if _has_localhost_cmd(rows):
        codes.append("localhost-cmd")
    return codes
