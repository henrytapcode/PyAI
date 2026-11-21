import pytest

import exercise


def test_clean_repo():
    snap = {"README.md": "# App", "main.py": "print(1)"}
    status = exercise.git_status(snap, dict(snap), dict(snap))
    assert status == {
        "staged": [],
        "untracked": [],
        "modified": [],
        "deleted": [],
    }


def test_status_all_categories_sorted():
    committed = {"a.py": "1", "b.py": "2", "old.py": "x"}
    staged = {"a.py": "1-staged", "b.py": "2", "c.py": "3"}
    working = {"a.py": "1-staged", "b.py": "2-work", "z.py": "9", "m.py": "5"}
    status = exercise.git_status(committed, staged, working)
    assert status == {
        "staged": ["a.py", "c.py", "old.py"],
        "untracked": ["m.py", "z.py"],
        "modified": ["b.py"],
        "deleted": ["c.py"],
    }


def test_stage_files_add_modify_and_delete():
    staged = {"a.py": "v1", "old.py": "gone"}
    working = {"a.py": "v2", "new.py": "hi"}
    updated = exercise.stage_files(staged, working, ["a.py", "new.py", "old.py"])
    assert updated == {"a.py": "v2", "new.py": "hi"}
    assert staged == {"a.py": "v1", "old.py": "gone"}


def test_stage_files_missing_raises_key_error():
    with pytest.raises(KeyError):
        exercise.stage_files({"a.py": "1"}, {"a.py": "1"}, ["missing.py"])
