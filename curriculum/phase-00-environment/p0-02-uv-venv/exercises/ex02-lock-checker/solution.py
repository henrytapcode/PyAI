def check_venv_isolation(
    envs: dict[str, dict[str, str]],
    project: str,
    package: str,
    expected_version: str,
) -> dict:
    if project not in envs:
        return {"ok": False, "status": "unknown_env", "installed": None}

    normalized = {name.lower(): ver for name, ver in envs[project].items()}
    installed_ver = normalized.get(package.lower())
    if installed_ver is None:
        return {"ok": False, "status": "missing_package", "installed": None}

    if installed_ver != expected_version:
        return {"ok": False, "status": "version_mismatch", "installed": installed_ver}

    return {"ok": True, "status": "ok", "installed": installed_ver}


def diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]:
    added = sorted(pkg for pkg in new_lock if pkg not in old_lock)
    removed = sorted(pkg for pkg in old_lock if pkg not in new_lock)
    changed = sorted(
        pkg for pkg in old_lock if pkg in new_lock and old_lock[pkg] != new_lock[pkg]
    )
    return {"added": added, "removed": removed, "changed": changed}
