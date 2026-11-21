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
        if input_per_1k < 0 or output_per_1k < 0:
            raise ValueError("pricing rates must be non-negative")
        self.input_per_1k = float(input_per_1k)
        self.output_per_1k = float(output_per_1k)


class CostBudget:
    """Tracks cumulative token usage and USD cost against hard caps."""

    def __init__(self, max_tokens: int, max_cost_usd: float) -> None:
        if max_tokens <= 0 or max_cost_usd <= 0:
            raise ValueError("budget limits must be positive")
        self.max_tokens = int(max_tokens)
        self.max_cost_usd = float(max_cost_usd)
        self.total_tokens = 0
        self.cost_usd = 0.0

    def record(self, usage: Usage, pricing: Pricing) -> float:
        step_cost = (
            usage.prompt_tokens * pricing.input_per_1k
            + usage.completion_tokens * pricing.output_per_1k
        ) / 1000.0
        self.total_tokens += usage.total_tokens
        self.cost_usd = round(self.cost_usd + step_cost, 6)
        return round(step_cost, 6)

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
    """Call ``fn`` with exponential backoff on transient errors when idempotent."""
    if max_retries < 0 or base_delay < 0:
        raise ValueError("max_retries and base_delay must be non-negative")
    max_attempts = max_retries + 1 if idempotent else 1
    wait_seconds = 0.0
    attempts = 0
    for attempt in range(max_attempts):
        attempts += 1
        try:
            value = fn()
            return {
                "ok": True,
                "value": value,
                "error": None,
                "attempts": attempts,
                "wait_seconds": wait_seconds,
            }
        except (RateLimitError, TimeoutError) as exc:
            if not idempotent or attempt >= max_retries:
                return {
                    "ok": False,
                    "value": None,
                    "error": str(exc),
                    "attempts": attempts,
                    "wait_seconds": wait_seconds,
                }
            delay = base_delay * (2**attempt)
            clock.advance(delay)
            wait_seconds += delay
        except Exception as exc:
            return {
                "ok": False,
                "value": None,
                "error": str(exc),
                "attempts": attempts,
                "wait_seconds": wait_seconds,
            }
    return {
        "ok": False,
        "value": None,
        "error": "retry loop exhausted",
        "attempts": attempts,
        "wait_seconds": wait_seconds,
    }


def _agent_outcome(
    answer: str | None,
    stopped_reason: str,
    steps: int,
    budget: CostBudget,
    retries: int,
) -> dict[str, Any]:
    return {
        "answer": answer,
        "stopped_reason": stopped_reason,
        "steps": steps,
        "total_tokens": budget.total_tokens,
        "cost_usd": budget.cost_usd,
        "retries": retries,
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
    """Run a tool-using agent loop guarded by idempotent retries and CostBudget."""
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    steps = 0
    retries = 0

    for _ in range(max_steps):
        reason = budget.check()
        if reason is not None:
            return _agent_outcome(None, reason, steps, budget, retries)

        res = call_with_retry(
            lambda: client.chat(messages, tools=tools),
            clock,
            max_retries=max_retries,
            idempotent=True,
        )
        retries += res["attempts"] - 1
        if not res["ok"]:
            return _agent_outcome(None, "rate_limit", steps, budget, retries)

        resp = res["value"]
        steps += 1
        budget.record(resp.usage, pricing)

        reason = budget.check()
        if reason is not None:
            return _agent_outcome(None, reason, steps, budget, retries)

        if not resp.tool_calls:
            return _agent_outcome(resp.content, "final", steps, budget, retries)

        messages.append({"role": "assistant", "content": resp.content or ""})
        for tc in resp.tool_calls:
            outcome = registry.execute(tc.name, tc.arguments, ctx)
            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(outcome, sort_keys=True),
                }
            )

    return _agent_outcome(None, "max_steps", steps, budget, retries)
