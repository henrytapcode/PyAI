import pytest

import exercise


def test_p50_odd_and_even_lists():
    assert exercise.percentile([100, 200, 300], 50) == 200.0
    assert exercise.percentile([10, 20, 30, 40], 50) == 20.0


def test_p95_for_twenty_values_and_report():
    values = [float(i * 10) for i in range(1, 21)]
    assert exercise.percentile(values, 95) == 190.0
    assert exercise.latency_report(values) == {"p50": 100.0, "p95": 190.0, "max": 200.0}


def test_percentile_is_order_independent():
    values = [180.0, 210.0, 350.0, 195.0, 420.0]
    reversed_values = list(reversed(values))
    assert exercise.percentile(values, 95) == exercise.percentile(reversed_values, 95)
    assert values == [180.0, 210.0, 350.0, 195.0, 420.0], "input list should not be mutated"


def test_percentile_100_returns_max():
    values = [240.0, 180.0, 950.0, 310.0]
    assert exercise.percentile(values, 100) == 950.0


def test_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        exercise.percentile([], 50)
    with pytest.raises(ValueError):
        exercise.percentile([100.0], 0)
    with pytest.raises(ValueError):
        exercise.percentile([100.0], 101)
