# Take n items at a time with islice

This uses a standard-library tool this course does not cover: `islice(iterator, n)` from the `itertools` module takes up to `n` items from an iterator. `iter(items)` makes the bookmark from §1, `list(...)` collects the slice, and an empty batch means the input is finished. A bare `return` inside a generator simply ends it. It is shorter than the manual version and just as lazy, but you need to know `islice` and the `while True` pattern, so the plain loop is easier to read for a beginner.
