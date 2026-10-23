def batched(items, n):
    """Yield the items in lists of up to n items, one list at a time.

    Example: list(batched([1, 2, 3, 4, 5], 2)) gives [[1, 2], [3, 4], [5]]
    """
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch
