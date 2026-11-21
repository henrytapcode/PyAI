import exercise


def test_clean_merge_with_deletions_and_identical_edits():
    base = {"keep.py": "v1", "del_feat.py": "old", "both.py": "0"}
    main = {"keep.py": "v1-main", "del_feat.py": "old", "both.py": "1"}
    feature = {"keep.py": "v1", "both.py": "1", "new.py": "added"}
    result = exercise.three_way_merge(base, main, feature)
    assert result == {
        "merged": {"keep.py": "v1-main", "both.py": "1", "new.py": "added"},
        "conflicts": [],
    }


def test_merge_conflicts_sorted_and_deletion_conflict():
    base = {"z.py": "1", "a.py": "1", "del_vs_edit.py": "base"}
    main = {"z.py": "2", "a.py": "main"}
    feature = {"z.py": "3", "a.py": "feat", "del_vs_edit.py": "feat-edit"}
    result = exercise.three_way_merge(base, main, feature)
    assert result["conflicts"] == ["a.py", "del_vs_edit.py", "z.py"]
    assert result["merged"] == {"a.py": "main", "z.py": "2"}


def test_valid_commit_messages():
    assert exercise.is_valid_commit_msg("Add git status helper") is True
    assert exercise.is_valid_commit_msg("  Fix merge bug\n\nLonger body.") is True
    assert exercise.is_valid_commit_msg("a" * 72) is True


def test_invalid_commit_messages():
    assert exercise.is_valid_commit_msg("") is False
    assert exercise.is_valid_commit_msg("   \nBody") is False
    assert exercise.is_valid_commit_msg("Add feature.") is False
    assert exercise.is_valid_commit_msg("123 fix bug") is False
    assert exercise.is_valid_commit_msg("Đẩy code lên GitHub") is False
    assert exercise.is_valid_commit_msg("a" * 73) is False
