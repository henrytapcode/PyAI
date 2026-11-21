import re
import tomllib

_DEP_PATTERN = re.compile(
    r"^\s*([A-Za-z0-9._-]+)(?:\[[^\]]*\])?\s*(==|>=|<=|~=|!=|>|<)?\s*(.*?)\s*$"
)


def parse_dependencies(toml_text: str) -> dict[str, str]:
    data = tomllib.loads(toml_text)
    deps = data.get("project", {}).get("dependencies", [])
    parsed: dict[str, str] = {}
    for item in deps:
        match = _DEP_PATTERN.match(item)
        if match:
            name, op, ver = match.groups()
            parsed[name.lower()] = f"{op}{ver}" if op else ""
    return parsed


def missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]:
    req_set = {name.lower() for name in required}
    inst_set = {name.lower() for name in installed}
    return sorted(req_set - inst_set)
