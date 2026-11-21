from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pyai_llm import FakeLLM, RateLimitError, Usage

RETRYABLE_ERRORS = (RateLimitError, TimeoutError)


class FakeClock:
    """Deterministic virtual clock for testing exponential backoff."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = float(start)

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> float:
        self.t += float(seconds)
        return self.t


@dataclass(frozen=True)
class Pricing:
    """Immutable per-1k token pricing rates in USD."""

    input_per_1k: float
    output_per_1k: float

    def __post_init__(self) -> None:
        if self.input_per_1k < 0 or self.output_per_1k < 0:
            raise ValueError("pricing rates must be non-negative")


@dataclass
class CostBudget:
    """Dataclass-backed token and USD cost budget tracker."""

    max_tokens: int
    max_cost_usd: float
    total_tokens: int = 0
    cost_usd: float = 0.0

    def __post_init__(self) -> None:
        if self.max_tokens <= 0 or self.max_cost_usd <= 0:
            raise ValueError("budget limits must be positive")

    def record(self, usage: Usage, pricing: Pricing) -> float:
        delta_cost = (
            usage.prompt_tokens * pricing.input_per_1k
            + usage.completion_tokens * pricing.output_per_1k
        ) / 1000.0
        self.total_tokens += usage.total_tokens
        self.cost_usd = round(self.cost_usd + delta_cost, 6)
        return round(delta_cost, 6)

    def check(self) -> str | None:
        if self.total_tokens > self.max_tokens:
            return "token_budget"
        if self.cost_usd > self.max_cost_usd:
            return "cost_budget"
        return None


def call_with_retry(
    fn: Callable[[], Any],
    clock: FakeClock,
    max_retries: int = 3,
    base_delay: float = 0.5,
    idempotent: bool = True,
) -> dict[str, Any]:
    """Execute ``fn`` using a while-loop exponential backoff when idempotent."""
    if max_retries < 0 or base_delay < 0:
        raise ValueError("max_retries and base_delay must be non-negative")
    attempts = 0
    wait_seconds = 0.0
    delay = float(base_delay)

    while True:
        attempts += 1
        try:
            result = fn()
            return {
                "ok": True,
                "value": result,
                "error": None,
                "attempts": attempts,
                "wait_seconds": wait_seconds,
            }
        except RETRYABLE_ERRORS as exc:
            retries_used = attempts - 1
            if not idempotent or retries_used >= max_retries:
                return {
                    "ok": False,
                    "value": None,
                    "error": str(exc),
                    "attempts": attempts,
                    "wait_seconds": wait_seconds,
                }
            clock.advance(delay)
            wait_seconds += delay
            delay *= 2.0
        except Exception as exc:
            return {
                "ok": False,
                "value": None,
                "error": str(exc),
                "attempts": attempts,
                "wait_seconds": wait_seconds,
            }


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
    """Run a budgeted tool-using agent loop with a while-step counter."""
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    steps = 0
    retries = 0

    while steps < max_steps:
        breach = budget.check()
        if breach is not None:
            return {
                "answer": None,
                "stopped_reason": breach,
                "steps": steps,
                "total_tokens": budget.total_tokens,
                "cost_usd": budget.cost_usd,
                "retries": retries,
            }

        res = call_with_retry(
            lambda: client.chat(messages, tools=tools),
            clock,
            max_retries=max_retries,
            idempotent=True,
        )
        retries += res["attempts"] - 1
        if not res["ok"]:
            return {
                "answer": None,
                "stopped_reason": "rate_limit",
                "steps": steps,
                "total_tokens": budget.total_tokens,
                "cost_usd": budget.cost_usd,
                "retries": retries,
            }

        resp = res["value"]
        steps += 1
        budget.record(resp.usage, pricing)

        breach = budget.check()
        if breach is not None:
            return {
                "answer": None,
                "stopped_reason": breach,
                "steps": steps,
                "total_tokens": budget.total_tokens,
                "cost_usd": budget.cost_usd,
                "retries": retries,
            }

        if not resp.tool_calls:
            return {
                "answer": resp.content,
                "stopped_reason": "final",
                "steps": steps,
                "total_tokens": budget.total_tokens,
                "cost_usd": budget.cost_usd,
                "retries": retries,
            }

        messages.append({"role": "assistant", "content": resp.content or ""})
        for tc in resp.tool_calls:
            outcome = registry.execute(tc.name, tc.arguments, ctx)
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(outcome, sort_keys=True),
                }
            )

    return {
        "answer": None,
        "stopped_reason": "max_steps",
        "steps": steps,
        "total_tokens": budget.total_tokens,
        "cost_usd": budget.cost_usd,
        "retries": retries,
    }
