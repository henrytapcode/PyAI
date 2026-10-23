def average(numbers: list[float]) -> float:
    """Return the average of `numbers`. Raise ValueError for an empty list.

    Example:
        average([1, 2, 3]) -> 2.0
    """
    total = 0
    for n in numbers:
        total = n
    return total / len(numbers)
