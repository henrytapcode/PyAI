def find_python_files(entries: list[str], folder: str = "") -> list[str]:
    """Return sorted .py paths under normalized folder on a '/' boundary."""
    clean_folder = folder.strip().strip("/")
    prefix = f"{clean_folder}/" if clean_folder else ""
    matches: list[str] = []
    for entry in entries:
        path = entry.strip().lstrip("/")
        if not path.endswith(".py"):
            continue
        if prefix and not path.startswith(prefix):
            continue
        matches.append(path)
    return sorted(matches)


def build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]:
    """Build a python or uv run python command list for a .py script."""
    clean_script = script.strip()
    if not clean_script.endswith(".py"):
        raise ValueError(f"Expected a .py script, got: {script!r}")
    base = ["uv", "run", "python", clean_script] if use_uv else ["python", clean_script]
    if args:
        base.extend(args)
    return base
