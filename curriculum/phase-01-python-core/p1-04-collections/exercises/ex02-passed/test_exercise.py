from exercise import passed


def test_returns_names_not_scores():
    assert passed({"Lan": 9}, 5) == ["Lan"]


def test_score_equal_to_threshold_passes():
    assert passed({"Lan": 5, "Hoa": 3}, 5) == ["Lan"]


def test_result_is_sorted():
    assert passed({"Minh": 8, "Lan": 5, "Hoa": 3}, 5) == ["Lan", "Minh"]


def test_nobody_passes():
    assert passed({"Lan": 1, "Hoa": 2}, 5) == []


def test_empty_dict_gives_empty_list():
    assert passed({}, 5) == []
