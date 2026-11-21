# Record per-step JSONL spans and format a compact SRE summary report.
import json
import math
from collections.abc import Callable
from typing import Any


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = float(start)

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> float:
        self.t = round(self.t + seconds, 6)
        return self.t


class TraceRecorder:
    def __init__(self, clock: FakeClock) -> None:
        self.clock = clock
        self.spans: list[dict[str, Any]] = []

    def record_step(
        self,
        request_id: str,
        step: int,
        kind: str,
        name: str,
        fn: Callable[[], Any],
        tokens: int = 0,
        cost_usd: float = 0.0,
        retries: int = 0,
    ) -> tuple[Any, dict[str, Any]]:
        started_at = self.clock()
        try:
            result = fn()
            status, error = "ok", None
        except Exception as exc:
            result, status, error = None, "error", str(exc)
        duration_ms = round((self.clock() - started_at) * 1000.0, 3)
        span = {
            "request_id": request_id,
            "step": step,
            "kind": kind,
            "name": name,
            "status": status,
            "started_at": started_at,
            "duration_ms": duration_ms,
            "tokens": tokens,
            "cost_usd": cost_usd,
            "retries": retries,
            "error": error,
        }
        self.spans.append(span)
        return result, span

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(s, sort_keys=True) for s in self.spans)


def summarize_traces(spans: list[dict[str, Any]], budget_usd: float | None = None) -> dict[str, Any]:
    tool_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for s in spans:
        status_counts[s["status"]] = status_counts.get(s["status"], 0) + 1
        if s["kind"] == "tool":
            tool_counts[s["name"]] = tool_counts.get(s["name"], 0) + 1
    durs = sorted(s["duration_ms"] for s in spans)
    p95 = 0.0 if not durs else durs[max(0, math.ceil(0.95 * len(durs)) - 1)]
    total_cost = round(sum(s["cost_usd"] for s in spans), 6)
    util = round(total_cost / budget_usd, 6) if budget_usd is not None and budget_usd > 0 else None
    return {
        "total_requests": len({s["request_id"] for s in spans}),
        "total_steps": len(spans),
        "tool_counts": tool_counts,
        "status_counts": status_counts,
        "total_retries": sum(s["retries"] for s in spans),
        "total_tokens": sum(s["tokens"] for s in spans),
        "total_cost_usd": total_cost,
        "p95_step_ms": p95,
        "budget_utilization": util,
        "failed_requests": sorted({s["request_id"] for s in spans if s["status"] == "error"}),
    }


def format_report(summary: dict[str, Any]) -> str:
    util = "n/a" if summary["budget_utilization"] is None else f"{summary['budget_utilization'] * 100:.1f}%"
    lines = [
        f"Requests: {summary['total_requests']} | Steps: {summary['total_steps']}",
        f"Tokens: {summary['total_tokens']} | Cost: ${summary['total_cost_usd']:.4f} ({util})",
        f"Retries: {summary['total_retries']} | p95: {summary['p95_step_ms']} ms",
        f"Tools: {summary['tool_counts']}",
        f"Failed: {summary['failed_requests']}",
    ]
    return "\n".join(lines)


clock = FakeClock()
rec = TraceRecorder(clock)
rec.record_step("req-1", 1, "llm", "fake-llm", lambda: clock.advance(0.045), tokens=120, cost_usd=0.0004, retries=1)
rec.record_step("req-1", 2, "tool", "lookup_order", lambda: clock.advance(0.015))
rec.record_step("req-2", 1, "llm", "fake-llm", lambda: clock.advance(0.030), tokens=90, cost_usd=0.0003)
rec.record_step("req-2", 2, "tool", "issue_refund", lambda: (_ for _ in ()).throw(RuntimeError("gateway down")))

print("JSONL spans:")
print(rec.to_jsonl())
summary = summarize_traces(rec.spans, budget_usd=0.01)
print("\nReport:")
print(format_report(summary))
