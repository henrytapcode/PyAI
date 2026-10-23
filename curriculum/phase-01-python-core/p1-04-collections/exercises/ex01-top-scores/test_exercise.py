from exercise import top_scores


def test_returns_the_biggest_first():
    assert top_scores([0.5, 0.9, 0.7, 0.8], 2) == [0.9, 0.8], "sort biggest first, then keep n"


def test_returns_everything_when_n_is_larger_than_the_list():
    assert top_scores([3, 1, 2], 5) == [3, 2, 1]


def test_empty_list_gives_empty_list():
    assert top_scores([], 3) == []


def test_n_zero_gives_empty_list():
    assert top_scores([4, 8], 0) == []


def test_keeps_duplicate_scores():
    assert top_scores([5, 9, 5, 9, 1], 3) == [9, 9, 5]


def test_does_not_change_the_original_list():
    scores = [3, 1, 2]
    top_scores(scores, 2)
    assert scores == [3, 1, 2], "use sorted(), not scores.sort(), so the original is left alone"
