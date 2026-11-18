import pytest

import exercise


@pytest.mark.parametrize(
    "prompt_tokens,completion_tokens,expected_cost",
    [
        (1000, 0, 0.0005),
        (0, 1000, 0.0015),
        (1000, 500, 0.00125),
        (200, 400, 0.0007),
    ],
)
def test_record_returns_request_cost(prompt_tokens, completion_tokens, expected_cost):
    tracker = exercise.MetricsTracker(price_in_per_1k=0.0005, price_out_per_1k=0.0015)
    cost = tracker.record(
        latency_ms=200.0,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    assert cost == pytest.approx(expected_cost)


def test_summary_aggregates_total_cost_and_count():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    tracker.record(100.0, 500, 250)
    tracker.record(200.0, 1000, 500)
    summary = tracker.summary()
    assert summary is not None
    assert summary["count"] == 2
    assert summary["error_rate"] == pytest.approx(0.0)
    assert summary["total_cost"] == pytest.approx(0.003)


def test_failed_requests_count_toward_error_rate_latency_and_cost():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    tracker.record(150.0, 1000, 0, ok=True)
    tracker.record(900.0, 1000, 0, ok=False)
    summary = tracker.summary()
    assert summary is not None
    assert summary["count"] == 2
    assert summary["error_rate"] == pytest.approx(0.5)
    assert summary["p95_ms"] == pytest.approx(900.0)
    assert summary["total_cost"] == pytest.approx(0.002)


def test_summary_computes_nearest_rank_p95():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    for ms in reversed(range(100, 2100, 100)):
        tracker.record(float(ms), 100, 50)
    summary = tracker.summary()
    assert summary is not None
    assert summary["count"] == 20
    assert summary["p95_ms"] == pytest.approx(1900.0)


def test_empty_summary_returns_zeros():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    assert tracker.summary() == {
        "count": 0,
        "error_rate": 0.0,
        "p95_ms": 0.0,
        "total_cost": 0.0,
    }


def test_alerts_empty_when_healthy():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    for _ in range(20):
        tracker.record(200.0, 100, 100, ok=True)
    assert tracker.alerts(max_p95_ms=500.0, budget=1.0) == []


@pytest.mark.parametrize(
    "latency_ms,prompt_tokens,ok_flags,expected",
    [
        (800.0, 100, [True], ["p95-latency"]),
        (200.0, 8000, [True], ["budget-warning"]),
        (200.0, 12000, [True], ["budget-exceeded"]),
        (200.0, 100, [True, False], ["error-rate"]),
    ],
)
def test_alerts_single_conditions(latency_ms, prompt_tokens, ok_flags, expected):
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    for ok in ok_flags:
        tracker.record(latency_ms, prompt_tokens, 0, ok=ok)
    assert tracker.alerts(max_p95_ms=500.0, budget=0.01) == expected


def test_budget_warning_and_exceeded_are_mutually_exclusive():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    tracker.record(100.0, 15000, 0, ok=True)
    alerts = tracker.alerts(max_p95_ms=500.0, budget=0.01, warn_ratio=0.8)
    assert alerts == ["budget-exceeded"]
    assert "budget-warning" not in alerts


def test_alerts_preserve_fixed_order_when_multiple_fire():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    tracker.record(1200.0, 9000, 0, ok=False)
    assert tracker.alerts(max_p95_ms=500.0, budget=0.01, warn_ratio=0.8) == [
        "p95-latency",
        "budget-warning",
        "error-rate",
    ]


@pytest.mark.parametrize(
    "latency_ms,prompt_tokens,ok_count,fail_count,expected",
    [
        # exact p95 boundary (500.0 == 500.0) must not alert
        (500.0, 100, 1, 0, []),
        # just above p95 boundary (500.01 > 500.0) must alert
        (500.01, 100, 1, 0, ["p95-latency"]),
        # exact budget boundary (0.01 == 0.01) fires only budget-warning, not budget-exceeded
        (100.0, 10000, 1, 0, ["budget-warning"]),
        # just above budget boundary (0.010001 > 0.01) fires budget-exceeded
        (100.0, 10001, 1, 0, ["budget-exceeded"]),
        # exact error_rate boundary (1/20 == 0.05) must not alert
        (100.0, 10, 19, 1, []),
        # just above error_rate boundary (1/19 > 0.05) must alert
        (100.0, 10, 18, 1, ["error-rate"]),
    ],
)
def test_alerts_strict_boundaries(latency_ms, prompt_tokens, ok_count, fail_count, expected):
    tracker = exercise.MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
    for _ in range(ok_count):
        tracker.record(latency_ms, prompt_tokens, 0, ok=True)
    for _ in range(fail_count):
        tracker.record(latency_ms, prompt_tokens, 0, ok=False)
    assert tracker.alerts(max_p95_ms=500.0, budget=0.01, warn_ratio=0.8) == expected


def test_summary_rounds_total_cost_to_six_decimals():
    tracker = exercise.MetricsTracker(price_in_per_1k=0.000123, price_out_per_1k=0.000456)
    tracker.record(100.0, 100, 100)
    summary = tracker.summary()
    assert summary is not None
    assert summary["total_cost"] == 0.000058
