import ___
from collections import ___
from datetime import ___


def top_words(text, n):
    """Return the n most common words as (word, count) pairs.

    Example: top_words("the cat the dog the end", 1) -> [("the", 3)]
    """
    counts = ___(text.lower().split())
    return counts.___(n)


def days_until(today, deadline):
    """Return how many days from today to deadline (both are date objects).

    Example: days_until(date(2025, 4, 1), date(2025, 4, 15)) -> 14
    """
    return (deadline - today).___


def deadline_after(start, days):
    """Return the date that is `days` days after `start` (a date object).

    Example: deadline_after(date(2025, 3, 1), 45) -> date(2025, 4, 15)
    """
    return start + ___(days=days)


def pick(items, seed):
    """Pick one item; the same seed always gives the same item.

    Example: pick(["a", "b", "c"], 7) twice -> the same item both times
    """
    rng = random.___(seed)
    return rng.___(items)
