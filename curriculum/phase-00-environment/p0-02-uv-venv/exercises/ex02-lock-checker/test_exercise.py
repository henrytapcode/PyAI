import exercise


def test_check_venv_isolation_all_statuses():
    envs = {
        "chatbot": {"httpx": "0.25.0", "PyYAML": "6.0.1"},
        "evals": {"httpx": "0.27.0", "pytest": "8.2.0"},
    }
    assert exercise.check_venv_isolation(envs, "unknown", "httpx", "0.27.0") == {
        "ok": False,
        "status": "unknown_env",
        "installed": None,
    }
    assert exercise.check_venv_isolation(envs, "chatbot", "pytest", "8.2.0") == {
        "ok": False,
        "status": "missing_package",
        "installed": None,
    }
    assert exercise.check_venv_isolation(envs, "chatbot", "httpx", "0.27.0") == {
        "ok": False,
        "status": "version_mismatch",
        "installed": "0.25.0",
    }
    assert exercise.check_venv_isolation(envs, "evals", "httpx", "0.27.0") == {
        "ok": True,
        "status": "ok",
        "installed": "0.27.0",
    }
    assert exercise.check_venv_isolation(envs, "chatbot", "pyyaml", "6.0.1") == {
        "ok": True,
        "status": "ok",
        "installed": "6.0.1",
    }


def test_diff_lockfiles_changes_and_sorting():
    old_lock = {"httpx": "0.25.0", "pydantic": "2.6.0", "rich": "13.7.0"}
    new_lock = {"httpx": "0.27.0", "pydantic": "2.6.0", "pytest": "8.2.0", "anyio": "4.3.0"}
    assert exercise.diff_lockfiles(old_lock, new_lock) == {
        "added": ["anyio", "pytest"],
        "removed": ["rich"],
        "changed": ["httpx"],
    }


def test_diff_lockfiles_identical_and_empty():
    lock = {"httpx": "0.27.0"}
    assert exercise.diff_lockfiles(lock, lock) == {
        "added": [],
        "removed": [],
        "changed": [],
    }
    assert exercise.diff_lockfiles({}, {}) == {
        "added": [],
        "removed": [],
        "changed": [],
    }
