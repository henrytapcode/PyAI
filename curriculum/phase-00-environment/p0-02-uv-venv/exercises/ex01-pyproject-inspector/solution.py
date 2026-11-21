import tomllib

_OPERATORS = ("==", ">=", "<=", "~=", "!=", ">", "<")


def _split_dep(entry: str) -> tuple[str, str]:
    for op in _OPERATORS:
        if op in entry:
            raw_name, raw_ver = entry.split(op, 1)
            name = raw_name.split("[", 1)[0].strip().lower()
            return name, f"{op}{raw_ver.strip()}"
    name = entry.split("[", 1)[0].strip().lower()
    return name, ""


def parse_dependencies(toml_text: str) -> dict[str, str]:
    data = tomllib.loads(toml_text)
    deps = data.get("project", {}).get("dependencies", [])
    result: dict[str, str] = {}
    for entry in deps:
        name, spec = _split_dep(entry)
        result[name] = spec
    return result


def missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]:
    installed_names = {pkg.lower() for pkg in installed}
    return sorted({pkg.lower() for pkg in required if pkg.lower() not in installed_names})
