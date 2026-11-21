import exercise


def test_find_first_above_basic():
    assert exercise.find_first_above([1.0, 5.0, 3.0], 2.0) == 1


def test_find_first_above_strict_boundary():
    assert exercise.find_first_above([2.0, 2.0, 5.0], 2.0) == 2


def test_find_first_above_not_found():
    assert exercise.find_first_above([1.0, 2.0], 5.0) is None
    assert exercise.find_first_above([], 0.0) is None


def test_trace_watch_hits_breakpoint():
    result = exercise.trace_watch([4, 7, 12, 9], 12)
    assert result == [
        {"index": 0, "value": 4, "running_sum": 4, "hit_breakpoint": False},
        {"index": 1, "value": 7, "running_sum": 11, "hit_breakpoint": False},
        {"index": 2, "value": 12, "running_sum": 23, "hit_breakpoint": True},
    ]


def test_trace_watch_no_hit():
    assert exercise.trace_watch([3, 5, 2], 99) == [
        {"index": 0, "value": 3, "running_sum": 3, "hit_breakpoint": False},
        {"index": 1, "value": 5, "running_sum": 8, "hit_breakpoint": False},
        {"index": 2, "value": 2, "running_sum": 10, "hit_breakpoint": False},
    ]
    assert exercise.trace_watch([], 5) == []
