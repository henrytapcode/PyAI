import pytest

import exercise


@pytest.mark.parametrize(
    "text, expected",
    [("banana", 3), ("python", 1), ("queue", 4), ("rhythm", 0), ("", 0)],
)
def test_counts_the_vowels(text, expected):
    assert exercise.count_vowels(text) == expected, f"count_vowels({text!r}) should be {expected}"


def test_counts_repeated_vowels_each_time():
    assert exercise.count_vowels("aaa") == 3
