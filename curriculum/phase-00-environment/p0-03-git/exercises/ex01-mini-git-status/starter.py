def git_status(
    committed: dict[str, str],
    staged: dict[str, str],
    working: dict[str, str],
) -> dict[str, list[str]]:
    raise NotImplementedError("Implement git_status")


def stage_files(
    staged: dict[str, str],
    working: dict[str, str],
    paths: list[str],
) -> dict[str, str]:
    raise NotImplementedError("Implement stage_files")
