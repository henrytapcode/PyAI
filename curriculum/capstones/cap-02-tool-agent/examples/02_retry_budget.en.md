# Idempotent LLM retries and hard cost budgets

**What it shows:** Retrying transient `RateLimitError` failures on `FakeLLM.chat()` with `FakeClock` exponential backoff while enforcing `CostBudget` caps and duck-typed tool dispatch.

**Step by step**
1. Lines 9–43 define `FakeClock`, `Pricing`, and `CostBudget` (`record(usage, pricing)` and `check()`).
2. Lines 46–57 implement `call_with_retry()` to retry `(RateLimitError, TimeoutError)` only when `idempotent=True`, advancing `clock` by `0.5 * 2**attempt`.
3. Lines 60–62 define a minimal duck-typed `StubRegistry` exposing `.execute(name, args, ctx)`.
4. Lines 65–85 implement `run_budgeted_agent()`, checking `budget.check()` before and after each LLM call and executing tool calls once without retries.
5. Lines 88–95 run two scenarios: recovering from `fail_times=2` transient errors (`clock: 1.5`) and halting immediately when `max_tokens=10` is exceeded.

**Notice:** In Run 1, two retries advance `FakeClock` by `0.5 + 1.0 = 1.5` seconds; in Run 2, the first LLM response uses `20` tokens, so `CostBudget` stops the loop with `"token_budget"` before a second step runs.

**Try it yourself:** Lower `CostBudget(max_tokens=500, max_cost_usd=0.05)` in Run 1 to `max_cost_usd=0.0001` and observe `stopped_reason` switch to `"cost_budget"`.
