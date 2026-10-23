import pytest

from exercise import last_n, reproduce


def test_reproduce_returns_a_list_and_a_number():
    items, n = reproduce()
    assert isinstance(items, list)
    assert isinstance(n, int)


def test_reproduce_uses_the_input_that_triggers_the_bug():
    items, n = reproduce()
    assert n == 0, "the bug only happens for one value of n: try small values and compare"
    assert len(items) == 1, "the smallest input that shows it has just one item"


@pytest.mark.parametrize(
    "items, n, expected",
    [
        ([1, 2, 3, 4], 2, [3, 4]),
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        ([1, 2, 3], 10, [1, 2, 3]),
        ([], 3, []),
        (["a"], 1, ["a"]),
    ],
)
def test_last_n_of_several_lists(items, n, expected):
    assert last_n(items, n) == expected


def test_zero_items_gives_an_empty_list():
    assert last_n([1, 2, 3, 4], 0) == [], "items[-0:] is the same as items[0:], the whole list"


def test_zero_on_a_single_item_gives_an_empty_list():
    assert last_n([1], 0) == []


def test_negative_n_raises_value_error():
    with pytest.raises(ValueError):
        last_n([1, 2, 3], -1)


def test_the_input_list_is_not_changed():
    items = [1, 2, 3]
    last_n(items, 2)
    last_n(items, 0)
    assert items == [1, 2, 3]
