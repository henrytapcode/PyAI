def batched(items, n):
    iterator = iter(items)
    batch = []
    while True:
        try:
            batch.append(next(iterator))
        except StopIteration:
            break
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch
