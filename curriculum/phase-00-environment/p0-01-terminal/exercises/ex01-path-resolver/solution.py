def resolve_path(cwd: str, target: str) -> str:
    """Resolve an absolute or relative POSIX path against cwd."""
    stack: list[str] = []
    if target.startswith("/"):
        raw_segments = target.split("/")
    else:
        raw_segments = cwd.split("/") + target.split("/")
    for seg in raw_segments:
        if seg in ("", "."):
            continue
        if seg == "..":
            if stack:
                stack.pop()
        else:
            stack.append(seg)
    return "/" + "/".join(stack)


def split_command(line: str) -> tuple[str, list[str]]:
    """Split a command line into (command, args), raising ValueError if blank."""
    tokens = line.strip().split()
    if not tokens:
        raise ValueError("Command cannot be empty")
    return tokens[0], tokens[1:]
