import json  # noqa: F401
import math  # noqa: F401
from collections.abc import Callable
from typing import Any


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
        raise NotImplementedError("Implement TraceRecorder.record_step")

    def to_jsonl(self) -> str:
        raise NotImplementedError("Implement TraceRecorder.to_jsonl")


def summarize_traces(
    spans: list[dict[str, Any]],
    budget_usd: float | None = None,
) -> dict[str, Any]:
    """Aggregate trace spans into latency, cost, and error summary metrics."""
    raise NotImplementedError("Implement summarize_traces")


def format_report(summary: dict[str, Any]) -> str:
    """Format a trace summary dictionary into a compact (< 60 chars/line) report."""
    raise NotImplementedError("Implement format_report")
