import json
import math
from collections.abc import Callable
from typing import Any

MAX_LINE_LEN = 60


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
        result: Any = None
        status = "ok"
        error: str | None = None
        try:
            result = fn()
        except Exception as exc:
            status = "error"
            error = str(exc)
        duration_ms = round((self.clock() - started_at) * 1000.0, 3)
        span: dict[str, Any] = {
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
        return "\n".join(json.dumps(span, sort_keys=True) for span in self.spans)


def summarize_traces(
    spans: list[dict[str, Any]],
    budget_usd: float | None = None,
) -> dict[str, Any]:
    """Aggregate trace spans into latency, cost, and error summary metrics."""
    tool_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    request_ids: set[str] = set()
    failed_set: set[str] = set()
    total_retries = 0
    total_tokens = 0
    raw_cost = 0.0
    durations: list[float] = []

    for span in spans:
        req_id = span["request_id"]
        request_ids.add(req_id)
        status = span["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "error":
            failed_set.add(req_id)
        if span["kind"] == "tool":
            tool_name = span["name"]
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        total_retries += span["retries"]
        total_tokens += span["tokens"]
        raw_cost += span["cost_usd"]
        durations.append(span["duration_ms"])

    total_cost_usd = round(raw_cost, 6)
    if not durations:
        p95_step_ms = 0.0
    else:
        durations.sort()
        p95_idx = max(0, math.ceil(0.95 * len(durations)) - 1)
        p95_step_ms = durations[p95_idx]

    budget_utilization: float | None = None
    if budget_usd is not None and budget_usd > 0:
        budget_utilization = round(total_cost_usd / budget_usd, 6)

    return {
        "total_requests": len(request_ids),
        "total_steps": len(spans),
        "tool_counts": tool_counts,
        "status_counts": status_counts,
        "total_retries": total_retries,
        "total_tokens": total_tokens,
        "total_cost_usd": total_cost_usd,
        "p95_step_ms": p95_step_ms,
        "budget_utilization": budget_utilization,
        "failed_requests": sorted(failed_set),
    }


def _fit_line(text: str) -> str:
    if len(text) < MAX_LINE_LEN:
        return text
    return text[: MAX_LINE_LEN - 4] + "..."


def format_report(summary: dict[str, Any]) -> str:
    """Format a trace summary dictionary into a compact (< 60 chars/line) report."""
    lines: list[str] = [
        "=== Trace Summary ===",
        _fit_line(f"Requests: {summary['total_requests']} | Steps: {summary['total_steps']}"),
        _fit_line(
            f"Tokens: {summary['total_tokens']} | Retries: {summary['total_retries']}"
        ),
        _fit_line(
            f"Cost: ${summary['total_cost_usd']:.6f} | P95: {summary['p95_step_ms']}ms"
        ),
    ]

    util = summary.get("budget_utilization")
    util_str = "n/a" if util is None else f"{util * 100:.2f}%"
    lines.append(_fit_line(f"Budget util: {util_str}"))

    status_counts = summary.get("status_counts", {})
    if status_counts:
        status_items = ", ".join(f"{k}={status_counts[k]}" for k in sorted(status_counts))
        lines.append(_fit_line(f"Statuses: {status_items}"))

    tool_counts = summary.get("tool_counts", {})
    if tool_counts:
        lines.append("Tools:")
        for tool_name in sorted(tool_counts):
            lines.append(_fit_line(f"  - {tool_name}: {tool_counts[tool_name]}"))
    else:
        lines.append("Tools: none")

    failed = summary.get("failed_requests", [])
    if failed:
        lines.append("Failed requests:")
        for req_id in failed:
            lines.append(_fit_line(f"  - {req_id}"))
    else:
        lines.append("Failed requests: none")

    return "\n".join(lines)
