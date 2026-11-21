def git_status(
    committed: dict[str, str],
    staged: dict[str, str],
    working: dict[str, str],
) -> dict[str, list[str]]:
    staged_changes: list[str] = []
    for path in sorted(set(committed) | set(staged)):
        if staged.get(path) != committed.get(path):
            staged_changes.append(path)

    untracked: list[str] = []
    modified: list[str] = []
    for path in sorted(working):
        if path not in committed and path not in staged:
            untracked.append(path)
        elif path in staged and working[path] != staged[path]:
            modified.append(path)

    deleted = sorted(set(staged) - set(working))
    return {
        "staged": staged_changes,
        "untracked": untracked,
        "modified": modified,
        "deleted": deleted,
    }


def stage_files(
    staged: dict[str, str],
    working: dict[str, str],
    paths: list[str],
) -> dict[str, str]:
    updated = staged.copy()
    for path in paths:
        if path in working:
            updated[path] = working[path]
        elif path in updated:
            updated.pop(path)
        else:
            raise KeyError(path)
    return updated
