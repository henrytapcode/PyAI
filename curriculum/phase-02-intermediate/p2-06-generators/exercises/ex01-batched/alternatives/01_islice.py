from itertools import islice


def batched(items, n):
    iterator = iter(items)
    while True:
        batch = list(islice(iterator, n))
        if not batch:
            return
        yield batch
