from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from pyai_llm import FakeLLM, RateLimitError, Usage


class FakeClock:
    """Deterministic virtual clock for testing exponential backoff."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = float(start)

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> float:
        self.t += float(seconds)
        return self.t


class Pricing:
    """Per-1k token pricing rates in USD."""

    def __init__(self, input_per_1k: float, output_per_1k: float) -> None:
        raise NotImplementedError("Implement Pricing.__init__")


class CostBudget:
    """Tracks cumulative token usage and USD cost against hard caps."""

    def __init__(self, max_tokens: int, max_cost_usd: float) -> None:
        raise NotImplementedError("Implement CostBudget.__init__")

    def record(self, usage: Usage, pricing: Pricing) -> float:
        raise NotImplementedError("Implement CostBudget.record")

    def check(self) -> str | None:
        raise NotImplementedError("Implement CostBudget.check")


def call_with_retry(
    fn: Callable[[], Any],
    clock: FakeClock,
    max_retries: int = 3,
    base_delay: float = 0.5,
    idempotent: bool = True,
) -> dict[str, Any]:
    """Call ``fn`` with exponential backoff on transient errors when idempotent."""
    raise NotImplementedError("Implement call_with_retry")


def run_budgeted_agent(
    task: str,
    client: FakeLLM,
    registry: Any,
    ctx: Any,
    clock: FakeClock,
    pricing: Pricing,
    budget: CostBudget,
    tools: list[dict[str, Any]] | None = None,
    max_steps: int = 5,
    max_retries: int = 2,
) -> dict[str, Any]:
    """Run a tool-using agent loop guarded by idempotent retries and CostBudget."""
    raise NotImplementedError("Implement run_budgeted_agent")
