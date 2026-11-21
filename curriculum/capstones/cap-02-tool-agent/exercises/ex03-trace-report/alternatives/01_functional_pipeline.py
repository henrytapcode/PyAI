import json
import math
from collections import Counter
from collections.abc import Callable
from typing import Any

LINE_LIMIT = 60


def _build_span(
    request_id: str,
    step: int,
    kind: str,
    name: str,
    status: str,
    started_at: float,
    ended_at: float,
    tokens: int,
    cost_usd: float,
    retries: int,
    error: str | None,
) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "step": step,
        "kind": kind,
        "name": name,
        "status": status,
        "started_at": started_at,
        "duration_ms": round((ended_at - started_at) * 1000.0, 3),
        "tokens": tokens,
        "cost_usd": cost_usd,
        "retries": retries,
        "error": error,
    }


def _nearest_rank_p95(durations: list[float]) -> float:
    if not durations:
        return 0.0
    ordered = sorted(durations)
    idx = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[idx]


def _clamp_line(line: str) -> str:
    return line if len(line) < LINE_LIMIT else line[: LINE_LIMIT - 4] + "..."


class TraceRecorder:
    """Record per-step execution spans using an injected clock."""

    def __init__(self, clock: Callable[[], float]) -> None:
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
            result = None
            status, error = "error", str(exc)
        span = _build_span(
            request_id=request_id,
            step=step,
            kind=kind,
            name=name,
            status=status,
            started_at=started_at,
            ended_at=self.clock(),
            tokens=tokens,
            cost_usd=cost_usd,
            retries=retries,
            error=error,
        )
        self.spans.append(span)
        return result, span

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(s, sort_keys=True) for s in self.spans)


def summarize_traces(
    spans: list[dict[str, Any]],
    budget_usd: float | None = None,
) -> dict[str, Any]:
    """Aggregate trace spans using Counter and pure helper functions."""
    tool_counts = dict(Counter(s["name"] for s in spans if s["kind"] == "tool"))
    status_counts = dict(Counter(s["status"] for s in spans))
    total_cost_usd = round(sum(s["cost_usd"] for s in spans), 6)
    budget_utilization = (
        round(total_cost_usd / budget_usd, 6)
        if budget_usd is not None and budget_usd > 0
        else None
    )
    return {
        "total_requests": len({s["request_id"] for s in spans}),
        "total_steps": len(spans),
        "tool_counts": tool_counts,
        "status_counts": status_counts,
        "total_retries": sum(s["retries"] for s in spans),
        "total_tokens": sum(s["tokens"] for s in spans),
        "total_cost_usd": total_cost_usd,
        "p95_step_ms": _nearest_rank_p95([s["duration_ms"] for s in spans]),
        "budget_utilization": budget_utilization,
        "failed_requests": sorted({s["request_id"] for s in spans if s["status"] == "error"}),
    }


def format_report(summary: dict[str, Any]) -> str:
    """Format a trace summary dictionary into a compact (< 60 chars/line) report."""
    util = summary.get("budget_utilization")
    util_text = "n/a" if util is None else f"{util * 100:.2f}%"
    rows = [
        "=== Trace Summary ===",
        f"Requests: {summary['total_requests']} | Steps: {summary['total_steps']}",
        f"Tokens: {summary['total_tokens']} | Retries: {summary['total_retries']}",
        f"Cost: ${summary['total_cost_usd']:.6f} | P95: {summary['p95_step_ms']}ms",
        f"Budget util: {util_text}",
    ]
    status_counts = summary.get("status_counts", {})
    if status_counts:
        joined = ", ".join(f"{k}={status_counts[k]}" for k in sorted(status_counts))
        rows.append(f"Statuses: {joined}")
    tool_counts = summary.get("tool_counts", {})
    if tool_counts:
        rows.append("Tools:")
        rows.extend(f"  - {k}: {tool_counts[k]}" for k in sorted(tool_counts))
    else:
        rows.append("Tools: none")
    failed = summary.get("failed_requests", [])
    if failed:
        rows.append("Failed requests:")
        rows.extend(f"  - {req}" for req in failed)
    else:
        rows.append("Failed requests: none")
    return "\n".join(_clamp_line(r) for r in rows)
