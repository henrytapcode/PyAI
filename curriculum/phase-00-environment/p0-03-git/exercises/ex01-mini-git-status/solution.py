def git_status(
    committed: dict[str, str],
    staged: dict[str, str],
    working: dict[str, str],
) -> dict[str, list[str]]:
    staged_changes = [
        p for p in sorted(committed.keys() | staged.keys()) if staged.get(p) != committed.get(p)
    ]
    untracked = [p for p in sorted(working) if p not in committed and p not in staged]
    modified = [p for p in sorted(working) if p in staged and working[p] != staged[p]]
    deleted = [p for p in sorted(staged) if p not in working]
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
    result = dict(staged)
    for path in paths:
        if path in working:
            result[path] = working[path]
        elif path in result:
            del result[path]
        else:
            raise KeyError(path)
    return result
