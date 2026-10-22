import pytest

import exercise


@pytest.mark.parametrize(
    "n, expected",
    [(10, 30), (7, 12), (2, 2), (1, 0), (0, 0)],
)
def test_sums_the_even_numbers_up_to_n(n, expected):
    assert exercise.sum_of_evens(n) == expected


def test_includes_n_when_n_is_even():
    assert exercise.sum_of_evens(4) == 6


def test_returns_an_int():
    assert type(exercise.sum_of_evens(6)) is int
