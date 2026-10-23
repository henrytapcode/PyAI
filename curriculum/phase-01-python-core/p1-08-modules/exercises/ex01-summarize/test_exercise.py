import pytest

from exercise import same_average, summarize


def test_summary_has_all_four_keys():
    result = summarize([1, 2, 3])
    assert isinstance(result, dict), "return a dict, not None"
    assert set(result) == {"count", "mean", "median", "stdev"}


def test_summary_of_four_scores():
    result = summarize([70, 80, 90, 100])
    assert result["count"] == 4
    assert result["mean"] == pytest.approx(85)
    assert result["median"] == pytest.approx(85)
    assert result["stdev"] == 12.91, "round the stdev to 2 decimals"


def test_median_ignores_the_order_of_the_list():
    assert summarize([9, 1, 5])["median"] == 5


def test_stdev_of_one_two_three_is_one():
    assert summarize([1, 2, 3])["stdev"] == pytest.approx(1.0)


def test_same_average_survives_float_rounding():
    assert same_average([0.1, 0.2], [0.15]) is True


def test_different_averages_are_not_the_same():
    assert same_average([1, 2, 3], [5]) is False
    assert same_average([1, 2, 3], [2, 2]) is True
