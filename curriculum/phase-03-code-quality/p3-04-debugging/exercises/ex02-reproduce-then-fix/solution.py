def last_n(items: list, n: int) -> list:
    """Return the last `n` items of `items`.

    Example:
        last_n([1, 2, 3, 4], 2) -> [3, 4]
        last_n([1, 2, 3, 4], 0) -> []
    """
    if n < 0:
        raise ValueError("n must not be negative")
    if n == 0:
        return []
    return items[-n:]


def reproduce() -> tuple[list, int]:
    """Return the smallest call (items, n) that shows the bug in `last_n`.

    Example:
        reproduce() -> ([1, 2, 3], 2)   # not the answer: this call works fine
    """
    return [1], 0
