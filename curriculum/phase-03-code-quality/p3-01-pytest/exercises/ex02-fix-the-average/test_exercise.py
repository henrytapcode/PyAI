import pytest

from exercise import average


def test_average_of_three_whole_numbers():
    assert average([1, 2, 3]) == pytest.approx(2.0), "add every number, not just the last one"


def test_single_number_is_its_own_average():
    assert average([5]) == pytest.approx(5.0)


def test_decimals_are_compared_with_approx():
    assert average([0.1, 0.2]) == pytest.approx(0.15)


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([2, 4], 3.0),
        ([0, 0, 0], 0.0),
        ([10, 20, 30, 40], 25.0),
        ([-1, 1], 0.0),
    ],
)
def test_average_of_several_lists(numbers, expected):
    assert average(numbers) == pytest.approx(expected)


def test_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        average([])


def test_the_input_list_is_not_changed():
    numbers = [1, 2, 3]
    average(numbers)
    assert numbers == [1, 2, 3]
