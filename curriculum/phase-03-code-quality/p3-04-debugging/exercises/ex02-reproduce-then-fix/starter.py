def last_n(items: list, n: int) -> list:
    """Return the last `n` items of `items`.

    Example:
        last_n([1, 2, 3, 4], 2) -> [3, 4]
        last_n([1, 2, 3, 4], 0) -> []
    """
    return items[-n:]


def reproduce() -> tuple[list, int]:
    """Return the smallest call (items, n) that shows the bug in `last_n`.

    Example:
        reproduce() -> ([1, 2, 3], 2)   # not the answer: this call works fine
    """
    # TODO: find an input where last_n gives the wrong answer, and return it
    return [1, 2, 3], 2
