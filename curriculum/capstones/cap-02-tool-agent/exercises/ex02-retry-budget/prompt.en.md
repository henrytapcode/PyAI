Implement `Pricing`, `CostBudget`, `call_with_retry`, and `run_budgeted_agent` using the provided `FakeClock` and `pyai_llm` (`FakeLLM`, `RateLimitError`, `Usage`). This exercise is self-contained: `run_budgeted_agent` interacts with `registry` strictly through duck typing (`registry.execute(name, args, ctx)`), with zero imports from `ex01`.

**Example**

```python
from pyai_llm import FakeLLM, Usage

clock = FakeClock()
pricing = Pricing(input_per_1k=0.001, output_per_1k=0.002)
budget = CostBudget(max_tokens=500, max_cost_usd=0.01)

cost = budget.record(Usage(prompt_tokens=200, completion_tokens=50, total_tokens=250), pricing)
# cost -> 0.0003, budget.total_tokens -> 250, budget.check() -> None

res = call_with_retry(lambda: "ok", clock, max_retries=2, base_delay=0.5, idempotent=True)
# res -> {"ok": True, "value": "ok", "error": None, "attempts": 1, "wait_seconds": 0.0}
```

**Rules**

- Keep `FakeClock(start=0.0)` with `self.t`, `__call__() -> float`, and `advance(seconds: float) -> float`.
- **`Pricing(input_per_1k: float, output_per_1k: float)`:** raise `ValueError` if `input_per_1k < 0` or `output_per_1k < 0`.
- **`CostBudget(max_tokens: int, max_cost_usd: float)`:**
  - Raise `ValueError` if `max_tokens <= 0` or `max_cost_usd <= 0`.
  - Initialize `self.total_tokens = 0` and `self.cost_usd = 0.0`.
  - `record(usage: Usage, pricing: Pricing) -> float`: compute `cost = (usage.prompt_tokens * pricing.input_per_1k + usage.completion_tokens * pricing.output_per_1k) / 1000.0`, add `usage.total_tokens` to `self.total_tokens`, set `self.cost_usd = round(self.cost_usd + cost, 6)`, and return `round(cost, 6)`.
  - `check() -> str | None`: return `"token_budget"` if `self.total_tokens > self.max_tokens`, else `"cost_budget"` if `self.cost_usd > self.max_cost_usd`, else `None`.
- **`call_with_retry(fn, clock, max_retries: int = 3, base_delay: float = 0.5, idempotent: bool = True) -> dict`:**
  - Retry **only** `(RateLimitError, TimeoutError)` when `idempotent=True`, up to `max_retries` retries (`max_retries + 1` total attempts).
  - When `idempotent=False`, execute `fn()` at most once (never retry side-effect calls).
  - Between retries (`attempt = 0, 1, ...`), advance `clock.advance(base_delay * (2 ** attempt))` and accumulate `wait_seconds`.
  - Return `{"ok": bool, "value": Any, "error": str | None, "attempts": int, "wait_seconds": float}`.
- **`run_budgeted_agent(task, client, registry, ctx, clock, pricing, budget, tools=None, max_steps=5, max_retries=2) -> dict`:**
  - Start with `messages = [{"role": "user", "content": task}]`, `steps = 0`, `retries = 0`.
  - For each step up to `max_steps`:
    1. Check `reason = budget.check()`; if not `None`, return immediately with `answer=None` and `stopped_reason=reason`.
    2. Call `call_with_retry(lambda: client.chat(messages, tools=tools), clock, max_retries=max_retries, idempotent=True)` and add `res["attempts"] - 1` to `retries`. If `not res["ok"]`, return `answer=None`, `stopped_reason="rate_limit"`.
    3. Increment `steps += 1`, call `budget.record(resp.usage, pricing)`, and check `budget.check()` again; if not `None`, return `answer=None` and `stopped_reason=reason`.
    4. If `not resp.tool_calls`, return `answer=resp.content`, `stopped_reason="final"`.
    5. Otherwise append `{"role": "assistant", "content": resp.content or ""}` (an explicit string `"content"` is required by `FakeLLM.chat`), execute each tool call `tc` **once** via `registry.execute(tc.name, tc.arguments, ctx)` (never retry tool calls), and append `{"role": "tool", "content": json.dumps(outcome, sort_keys=True)}`.
  - If `max_steps` is exhausted without a final answer, return `answer=None`, `stopped_reason="max_steps"`.
  - Return shape: `{"answer": str | None, "stopped_reason": str, "steps": int, "total_tokens": int, "cost_usd": float, "retries": int}`.
