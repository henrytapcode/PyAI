import posixpath


def resolve_path(cwd: str, target: str) -> str:
    combined = target if target.startswith("/") else f"{cwd}/{target}"
    normalized = posixpath.normpath(combined)
    while normalized.startswith("//"):
        normalized = normalized[1:]
    return normalized


def split_command(line: str) -> tuple[str, list[str]]:
    parts = line.split()
    if not parts:
        raise ValueError("Empty command")
    cmd, *args = parts
    return cmd, args
