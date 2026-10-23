import random
from collections import Counter
from datetime import timedelta


def top_words(text, n):
    """Return the n most common words as (word, count) pairs."""
    counts = Counter(text.lower().split())
    return counts.most_common(n)


def days_until(today, deadline):
    """Return how many days from today to deadline (both are date objects)."""
    return (deadline - today).days


def deadline_after(start, days):
    """Return the date that is `days` days after `start` (a date object)."""
    return start + timedelta(days=days)


def pick(items, seed):
    """Pick one item; the same seed always gives the same item."""
    rng = random.Random(seed)
    return rng.choice(items)
