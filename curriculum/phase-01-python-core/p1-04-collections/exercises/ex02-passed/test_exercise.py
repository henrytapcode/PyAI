from exercise import passed


def test_returns_names_not_scores():
    result = passed({"Lan": 9}, 5)
    assert result == ["Lan"], "the list should hold names only, not (name, score) pairs"


def test_score_equal_to_threshold_passes():
    result = passed({"Lan": 5, "Hoa": 3}, 5)
    assert result == ["Lan"], "'at least' means >=, so a score equal to threshold passes"


def test_result_is_sorted():
    result = passed({"Minh": 8, "Lan": 5, "Hoa": 3}, 5)
    assert result == ["Lan", "Minh"], "sort the names alphabetically"


def test_nobody_passes():
    assert passed({"Lan": 1, "Hoa": 2}, 5) == []


def test_empty_dict_gives_empty_list():
    assert passed({}, 5) == []
