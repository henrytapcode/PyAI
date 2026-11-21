def check_venv_isolation(
    envs: dict[str, dict[str, str]],
    project: str,
    package: str,
    expected_version: str,
) -> dict:
    raise NotImplementedError("TODO: implement check_venv_isolation")


def diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]:
    raise NotImplementedError("TODO: implement diff_lockfiles")
