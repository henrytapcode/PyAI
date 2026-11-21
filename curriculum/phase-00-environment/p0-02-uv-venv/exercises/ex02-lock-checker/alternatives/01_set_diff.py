def check_venv_isolation(
    envs: dict[str, dict[str, str]],
    project: str,
    package: str,
    expected_version: str,
) -> dict:
    env = envs.get(project)
    if env is None:
        return {"ok": False, "status": "unknown_env", "installed": None}

    target = package.lower()
    installed_ver = next((ver for name, ver in env.items() if name.lower() == target), None)
    if installed_ver is None:
        return {"ok": False, "status": "missing_package", "installed": None}

    ok = installed_ver == expected_version
    status = "ok" if ok else "version_mismatch"
    return {"ok": ok, "status": status, "installed": installed_ver}


def diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]:
    old_keys = set(old_lock)
    new_keys = set(new_lock)
    return {
        "added": sorted(new_keys - old_keys),
        "removed": sorted(old_keys - new_keys),
        "changed": sorted(k for k in old_keys & new_keys if old_lock[k] != new_lock[k]),
    }
