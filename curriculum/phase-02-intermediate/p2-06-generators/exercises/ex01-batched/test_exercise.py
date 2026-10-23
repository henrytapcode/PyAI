import pytest

from exercise import batched


def tracked(items, seen):
    """Hand out items one by one and record every item that was read."""
    for item in items:
        seen.append(item)
        yield item


def test_splits_the_example_from_the_prompt():
    assert list(batched([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_gives_back_something_you_can_call_next_on():
    result = batched([1, 2, 3], 2)
    assert next(result) == [1, 2], "use yield so that next(...) gives the first batch"
    assert next(result) == [3]


def test_no_empty_batch_when_the_size_divides_evenly():
    assert list(batched([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_keeps_the_shorter_last_batch():
    result = list(batched([1, 2, 3, 4, 5, 6, 7], 3))
    assert result == [[1, 2, 3], [4, 5, 6], [7]], "do not forget the items left over after the loop"


def test_empty_input_gives_no_batches():
    assert list(batched([], 3)) == []


def test_batch_size_bigger_than_the_input():
    assert list(batched([1, 2], 10)) == [[1, 2]]


def test_batch_size_one():
    assert list(batched(["a", "b", "c"], 1)) == [["a"], ["b"], ["c"]]


def test_every_batch_is_a_list():
    batches = list(batched((1, 2, 3, 4), 2))
    assert batches, "expected two batches"
    assert all(isinstance(b, list) for b in batches)


def test_each_batch_is_its_own_list():
    batches = list(batched([1, 2, 3, 4], 2))
    assert batches == [[1, 2], [3, 4]], "start a new empty list instead of reusing the old one"


def test_works_on_strings_and_ranges():
    assert list(batched("abcde", 2)) == [["a", "b"], ["c", "d"], ["e"]]
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_does_not_change_the_input():
    original = [1, 2, 3, 4, 5]
    copy = list(original)
    list(batched(original, 2))
    assert original == copy


def test_is_lazy_and_reads_only_what_the_first_batch_needs():
    seen = []
    result = batched(tracked([1, 2, 3, 4, 5, 6], seen), 2)
    assert seen == [], "nothing should be read before the first next(...)"
    assert next(result) == [1, 2]
    assert seen == [1, 2], "the first batch needs only 2 items, do not read more"
    assert next(result) == [3, 4]
    assert seen == [1, 2, 3, 4]


@pytest.mark.parametrize("size, expected", [
        (1, [[1], [2], [3], [4]]),
        (2, [[1, 2], [3, 4]]),
        (3, [[1, 2, 3], [4]]),
        (4, [[1, 2, 3, 4]]),
    ])
def test_different_sizes(size, expected):
    assert list(batched([1, 2, 3, 4], size)) == expected
