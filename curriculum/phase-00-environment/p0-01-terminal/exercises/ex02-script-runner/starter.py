def find_python_files(entries: list[str], folder: str = "") -> list[str]:
    # TODO: return sorted .py files under folder on a "/" boundary
    raise NotImplementedError


def build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]:
    # TODO: validate .py suffix and build command token list
    raise NotImplementedError
