# Retry idempotent LLM calls with FakeClock backoff and enforce CostBudget.
import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from pyai_llm import FakeLLM, RateLimitError, Usage


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = float(start)

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> float:
        self.t = round(self.t + seconds, 6)
        return self.t


@dataclass(frozen=True)
class Pricing:
    input_per_1k: float
    output_per_1k: float


class CostBudget:
    def __init__(self, max_tokens: int, max_cost_usd: float) -> None:
        self.max_tokens = max_tokens
        self.max_cost_usd = max_cost_usd
        self.total_tokens = 0
        self.cost_usd = 0.0

    def record(self, usage: Usage, pricing: Pricing) -> float:
        step_cost = (usage.prompt_tokens * pricing.input_per_1k + usage.completion_tokens * pricing.output_per_1k) / 1000.0
        self.total_tokens += usage.total_tokens
        self.cost_usd = round(self.cost_usd + step_cost, 6)
        return round(step_cost, 6)

    def check(self) -> str | None:
        if self.total_tokens > self.max_tokens:
            return "token_budget"
        if self.cost_usd > self.max_cost_usd:
            return "cost_budget"
        return None


def call_with_retry(fn: Callable[[], Any], clock: FakeClock, max_retries: int = 3, base_delay: float = 0.5, idempotent: bool = True) -> dict[str, Any]:
    wait_seconds = 0.0
    attempts = 0
    while True:
        attempts += 1
        try:
            return {"ok": True, "value": fn(), "error": None, "attempts": attempts, "wait_seconds": wait_seconds}
        except (RateLimitError, TimeoutError) as exc:
            if not idempotent or attempts > max_retries:
                return {"ok": False, "value": None, "error": str(exc), "attempts": attempts, "wait_seconds": wait_seconds}
            delay = base_delay * (2 ** (attempts - 1))
            clock.advance(delay)
            wait_seconds = round(wait_seconds + delay, 6)


class StubRegistry:
    def execute(self, name: str, args: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
        return {"ok": True, "status": "ok", "result": {"tool": name, "args": args, "role": ctx["role"]}}


def run_budgeted_agent(task: str, client: FakeLLM, registry: Any, ctx: Any, clock: FakeClock, pricing: Pricing, budget: CostBudget, max_steps: int = 4) -> dict[str, Any]:
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    steps = 0
    retries = 0
    for _ in range(max_steps):
        if reason := budget.check():
            return {"answer": None, "stopped_reason": reason, "steps": steps, "total_tokens": budget.total_tokens, "cost_usd": budget.cost_usd, "retries": retries}
        res = call_with_retry(lambda: client.chat(messages), clock, max_retries=2, idempotent=True)
        retries += res["attempts"] - 1
        if not res["ok"]:
            return {"answer": None, "stopped_reason": "rate_limit", "steps": steps, "total_tokens": budget.total_tokens, "cost_usd": budget.cost_usd, "retries": retries}
        resp = res["value"]
        steps += 1
        budget.record(resp.usage, pricing)
        if reason := budget.check():
            return {"answer": None, "stopped_reason": reason, "steps": steps, "total_tokens": budget.total_tokens, "cost_usd": budget.cost_usd, "retries": retries}
        if not resp.tool_calls:
            return {"answer": resp.content, "stopped_reason": "final", "steps": steps, "total_tokens": budget.total_tokens, "cost_usd": budget.cost_usd, "retries": retries}
        messages.append({"role": "assistant", "content": resp.content or ""})
        for tc in resp.tool_calls:
            outcome = registry.execute(tc.name, tc.arguments, ctx)
            messages.append({"role": "tool", "content": json.dumps(outcome, sort_keys=True)})
    return {"answer": None, "stopped_reason": "max_steps", "steps": steps, "total_tokens": budget.total_tokens, "cost_usd": budget.cost_usd, "retries": retries}


pricing = Pricing(input_per_1k=0.002, output_per_1k=0.006)
clock = FakeClock()
llm_ok = FakeLLM(fail_times=2, script=[{"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "ORD-7"}}]}, "Order ORD-7 total is 42.0."])
run_ok = run_budgeted_agent("Check ORD-7", llm_ok, StubRegistry(), {"role": "support"}, clock, pricing, CostBudget(max_tokens=500, max_cost_usd=0.05))
print("Run 1 (transient errors):", run_ok, "clock:", clock())

llm_tight = FakeLLM(script=[{"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "ORD-8"}}]}, "Done."])
run_cap = run_budgeted_agent("Check ORD-8", llm_tight, StubRegistry(), {"role": "support"}, FakeClock(), pricing, CostBudget(max_tokens=10, max_cost_usd=0.05))
print("Run 2 (tight token cap):", run_cap)
