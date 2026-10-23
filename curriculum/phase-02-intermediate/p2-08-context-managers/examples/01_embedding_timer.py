# Time three fake embedding calls with a context manager and a fake clock.
from contextlib import contextmanager

ticks = iter([100.0, 100.4, 200.0, 203.5, 300.0, 300.2])


def fake_clock():
    return next(ticks)


@contextmanager
def timer(label, results, clock=fake_clock):
    start = clock()
    try:
        yield
    finally:
        results.append((label, round(clock() - start, 1)))


def fake_embed(texts):
    return [len(text) for text in texts]


timings = []

with timer("small batch", timings):
    sizes = fake_embed(["hello", "world"])
print(sizes)

with timer("big batch", timings):
    sizes = fake_embed(["a" * 10] * 3)
print(sizes)

try:
    with timer("broken batch", timings):
        fake_embed(["ok", None])
except TypeError:
    print("embedding failed")

for label, seconds in timings:
    print(f"{label}: {seconds}s")
