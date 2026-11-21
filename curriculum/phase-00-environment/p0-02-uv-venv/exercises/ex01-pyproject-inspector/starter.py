import tomllib


def parse_dependencies(toml_text: str) -> dict[str, str]:
    raise NotImplementedError("TODO: implement parse_dependencies")


def missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]:
    raise NotImplementedError("TODO: implement missing_packages")
