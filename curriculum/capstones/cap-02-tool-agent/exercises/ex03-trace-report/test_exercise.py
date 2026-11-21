import json

import pytest
from exercise import TraceRecorder, format_report, summarize_traces


class FakeClock:
    def __init__(self, start: float = 100.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def test_record_step_success_captures_span_and_duration():
    clock = FakeClock(start=10.0)
    recorder = TraceRecorder(clock)

    def run_tool():
        clock.advance(0.0255)
        return {"order_id": "ord-1", "status": "shipped"}

    result, span = recorder.record_step(
        request_id="req-1",
        step=1,
        kind="tool",
        name="lookup_order",
        fn=run_tool,
        tokens=120,
        cost_usd=0.00024,
        retries=1,
    )

    assert result == {"order_id": "ord-1", "status": "shipped"}
    assert span == {
        "request_id": "req-1",
        "step": 1,
        "kind": "tool",
        "name": "lookup_order",
        "status": "ok",
        "started_at": 10.0,
        "duration_ms": 25.5,
        "tokens": 120,
        "cost_usd": 0.00024,
        "retries": 1,
        "error": None,
    }
    assert recorder.spans == [span]


def test_record_step_exception_records_error_span_and_duration():
    clock = FakeClock(start=5.0)
    recorder = TraceRecorder(clock)

    def failing_step():
        clock.advance(0.012)
        raise RuntimeError("gateway timeout")

    result, span = recorder.record_step(
        request_id="req-2",
        step=2,
        kind="tool",
        name="issue_refund",
        fn=failing_step,
        retries=2,
    )

    assert result is None
    assert span["status"] == "error"
    assert span["error"] == "gateway timeout"
    assert span["duration_ms"] == 12.0
    assert span["retries"] == 2
    assert len(recorder.spans) == 1


def test_to_jsonl_empty_and_sorted_keys():
    clock = FakeClock()
    recorder = TraceRecorder(clock)
    assert recorder.to_jsonl() == ""

    recorder.record_step("req-1", 1, "llm", "fake-gpt", lambda: "hi", tokens=10, cost_usd=0.0001)
    clock.advance(0.005)
    recorder.record_step("req-1", 2, "tool", "lookup_order", lambda: "ok")

    jsonl = recorder.to_jsonl()
    lines = jsonl.splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == recorder.spans[0]
    assert json.loads(lines[1]) == recorder.spans[1]
    assert lines[0] == json.dumps(recorder.spans[0], sort_keys=True)


def test_summarize_traces_empty_spans():
    summary = summarize_traces([], budget_usd=1.0)
    assert summary == {
        "total_requests": 0,
        "total_steps": 0,
        "tool_counts": {},
        "status_counts": {},
        "total_retries": 0,
        "total_tokens": 0,
        "total_cost_usd": 0.0,
        "p95_step_ms": 0.0,
        "budget_utilization": 0.0,
        "failed_requests": [],
    }
    assert summarize_traces([], budget_usd=None)["budget_utilization"] is None


def test_summarize_traces_filters_only_tool_kind_and_sorts_failed_requests():
    spans = [
        {
            "request_id": "req-b",
            "step": 1,
            "kind": "llm",
            "name": "fake-gpt",
            "status": "ok",
            "started_at": 0.0,
            "duration_ms": 10.0,
            "tokens": 100,
            "cost_usd": 0.001,
            "retries": 1,
            "error": None,
        },
        {
            "request_id": "req-b",
            "step": 2,
            "kind": "tool",
            "name": "lookup_order",
            "status": "error",
            "started_at": 0.01,
            "duration_ms": 20.0,
            "tokens": 0,
            "cost_usd": 0.0,
            "retries": 0,
            "error": "not found",
        },
        {
            "request_id": "req-a",
            "step": 1,
            "kind": "tool",
            "name": "lookup_order",
            "status": "ok",
            "started_at": 0.05,
            "duration_ms": 30.0,
            "tokens": 0,
            "cost_usd": 0.0,
            "retries": 0,
            "error": None,
        },
        {
            "request_id": "req-a",
            "step": 2,
            "kind": "tool",
            "name": "issue_refund",
            "status": "error",
            "started_at": 0.08,
            "duration_ms": 40.0,
            "tokens": 0,
            "cost_usd": 0.0,
            "retries": 2,
            "error": "denied",
        },
        {
            "request_id": "req-a",
            "step": 3,
            "kind": "tool",
            "name": "issue_refund",
            "status": "error",
            "started_at": 0.12,
            "duration_ms": 50.0,
            "tokens": 0,
            "cost_usd": 0.0,
            "retries": 0,
            "error": "denied",
        },
    ]

    summary = summarize_traces(spans, budget_usd=0.01)
    assert summary["total_requests"] == 2
    assert summary["total_steps"] == 5
    assert summary["tool_counts"] == {"lookup_order": 2, "issue_refund": 2}
    assert "fake-gpt" not in summary["tool_counts"]
    assert summary["status_counts"] == {"ok": 2, "error": 3}
    assert summary["total_retries"] == 3
    assert summary["total_tokens"] == 100
    assert summary["total_cost_usd"] == 0.001
    assert summary["budget_utilization"] == pytest.approx(0.1)
    assert summary["failed_requests"] == ["req-a", "req-b"]


@pytest.mark.parametrize(
    ("durations", "expected_p95"),
    [
        ([42.0], 42.0),
        ([110.0, 12.0, 40.0, 18.5, 25.0], 110.0),
        ([float(i) for i in range(20, 0, -1)], 19.0),
        ([float(i) for i in range(1, 22)], 20.0),
    ],
)
def test_summarize_traces_p95_nearest_rank(durations, expected_p95):
    spans = [
        {
            "request_id": f"r-{idx}",
            "step": 1,
            "kind": "llm",
            "name": "model",
            "status": "ok",
            "started_at": 0.0,
            "duration_ms": dur,
            "tokens": 1,
            "cost_usd": 0.0,
            "retries": 0,
            "error": None,
        }
        for idx, dur in enumerate(durations)
    ]
    assert summarize_traces(spans)["p95_step_ms"] == expected_p95


@pytest.mark.parametrize("bad_budget", [None, 0, 0.0, -5.0])
def test_summarize_traces_budget_utilization_none_for_missing_or_non_positive(bad_budget):
    spans = [
        {
            "request_id": "r-1",
            "step": 1,
            "kind": "llm",
            "name": "model",
            "status": "ok",
            "started_at": 0.0,
            "duration_ms": 5.0,
            "tokens": 10,
            "cost_usd": 0.0001234,
            "retries": 0,
            "error": None,
        }
    ]
    summary = summarize_traces(spans, budget_usd=bad_budget)
    assert summary["total_cost_usd"] == 0.000123
    assert summary["budget_utilization"] is None


def test_format_report_is_deterministic_and_under_60_chars_per_line():
    spans = [
        {
            "request_id": "req-very-long-identifier-that-exceeds-sixty-characters-easily",
            "step": 1,
            "kind": "tool",
            "name": "very_long_tool_name_that_would_otherwise_exceed_sixty_characters",
            "status": "error",
            "started_at": 0.0,
            "duration_ms": 123.456,
            "tokens": 500,
            "cost_usd": 0.0025,
            "retries": 1,
            "error": "boom",
        }
    ]
    summary = summarize_traces(spans, budget_usd=0.01)
    report_a = format_report(summary)
    report_b = format_report(summary)

    assert report_a == report_b
    lines = report_a.splitlines()
    assert len(lines) >= 5
    assert all(len(line) < 60 for line in lines)
    assert "0.002500" in report_a
    assert "123.456ms" in report_a
    assert "25.00%" in report_a

    empty_report = format_report(summarize_traces([]))
    assert all(len(line) < 60 for line in empty_report.splitlines())
