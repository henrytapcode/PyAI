def find_python_files(entries: list[str], folder: str = "") -> list[str]:
    clean_folder = folder.strip().strip("/")
    prefix = f"{clean_folder}/" if clean_folder else ""
    normalized = [item.strip().lstrip("/") for item in entries]
    return sorted(
        path
        for path in normalized
        if path.endswith(".py") and (not prefix or path.startswith(prefix))
    )


def build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]:
    clean = script.strip()
    if not clean.endswith(".py"):
        raise ValueError("Script must be a .py file")
    runner = ["uv", "run", "python"] if use_uv else ["python"]
    return [*runner, clean, *(args or [])]
