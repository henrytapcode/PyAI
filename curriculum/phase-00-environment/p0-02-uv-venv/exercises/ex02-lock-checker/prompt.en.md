Implement two functions in `starter.py` to verify virtual environment isolation and compare lockfile snapshots:

1. **`check_venv_isolation(envs: dict[str, dict[str, str]], project: str, package: str, expected_version: str) -> dict`**
   - `envs` maps each project name to its `{package_name: version}` dictionary.
   - Return `{"ok": bool, "status": str, "installed": str | None}` according to these rules:
     - If `project` is not in `envs`: `{"ok": False, "status": "unknown_env", "installed": None}`
     - Look up `package` case-insensitively in `envs[project]`. If missing: `{"ok": False, "status": "missing_package", "installed": None}`
     - If installed version != `expected_version`: `{"ok": False, "status": "version_mismatch", "installed": installed_ver}`
     - Otherwise: `{"ok": True, "status": "ok", "installed": installed_ver}`

2. **`diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]`**
   - Compare two `{package: version}` lockfile mappings.
   - Return `{"added": [...], "removed": [...], "changed": [...]}` with all three lists sorted ascending:
     - `"added"`: packages in `new_lock` but not in `old_lock`
     - `"removed"`: packages in `old_lock` but not in `new_lock`
     - `"changed"`: packages in both whose version string changed

Press **Check** to run the tests.
