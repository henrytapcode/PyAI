import pytest
from datetime import date

from exercise import deadline_after, days_until, pick, top_words


def test_top_words_finds_the_most_common_word():
    assert top_words("the cat the dog the end", 1) == [("the", 3)]


def test_top_words_returns_n_pairs_in_order():
    result = top_words("a b a c b a", 2)
    assert result == [("a", 3), ("b", 2)]


def test_top_words_lowercases_the_text():
    assert top_words("Go go GO", 1) == [("go", 3)]


@pytest.mark.parametrize("today, deadline, expected", [
    (date(2025, 4, 1), date(2025, 4, 15), 14),
    (date(2025, 1, 31), date(2025, 3, 1), 29),
    (date(2025, 5, 5), date(2025, 5, 5), 0),
])
def test_days_until(today, deadline, expected):
    assert days_until(today, deadline) == expected


def test_days_until_is_a_plain_number():
    assert days_until(date(2025, 1, 1), date(2025, 1, 3)) == 2, "use .days to get a number"


def test_deadline_after_adds_days():
    assert deadline_after(date(2025, 3, 1), 45) == date(2025, 4, 15)
    assert deadline_after(date(2025, 12, 30), 3) == date(2026, 1, 2)


def test_pick_is_repeatable_for_the_same_seed():
    items = ["a", "b", "c", "d", "e"]
    first = [pick(items, 7) for _ in range(5)]
    assert len(set(first)) == 1, "the same seed must always give the same item"
    assert first[0] in items


def test_pick_can_differ_between_seeds():
    items = list(range(100))
    results = {pick(items, seed) for seed in range(20)}
    assert len(results) > 1, "different seeds should give different picks"
