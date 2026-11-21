Hãy cài đặt `Pricing`, `CostBudget`, `call_with_retry` và `run_budgeted_agent` cùng với `FakeClock` đã cho sẵn và `pyai_llm` (`FakeLLM`, `RateLimitError`, `Usage`). Bài tập này độc lập hoàn toàn: `run_budgeted_agent` giao tiếp với `registry` theo kiểu duck typing (`registry.execute(name, args, ctx)`), không import gì từ `ex01`.

**Ví dụ**

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

**Quy tắc**

- Giữ nguyên `FakeClock(start=0.0)` với thuộc tính `self.t`, `__call__() -> float` và `advance(seconds: float) -> float`.
- **`Pricing(input_per_1k: float, output_per_1k: float)`:** raise `ValueError` nếu `input_per_1k < 0` hoặc `output_per_1k < 0`.
- **`CostBudget(max_tokens: int, max_cost_usd: float)`:**
  - Raise `ValueError` nếu `max_tokens <= 0` hoặc `max_cost_usd <= 0`.
  - Khởi tạo `self.total_tokens = 0` và `self.cost_usd = 0.0`.
  - `record(usage: Usage, pricing: Pricing) -> float`: tính `cost = (usage.prompt_tokens * pricing.input_per_1k + usage.completion_tokens * pricing.output_per_1k) / 1000.0`, cộng `usage.total_tokens` vào `self.total_tokens`, cập nhật `self.cost_usd = round(self.cost_usd + cost, 6)` và trả về `round(cost, 6)`.
  - `check() -> str | None`: trả về `"token_budget"` nếu `self.total_tokens > self.max_tokens`, ngược lại `"cost_budget"` nếu `self.cost_usd > self.max_cost_usd`, còn lại trả về `None`.
- **`call_with_retry(fn, clock, max_retries: int = 3, base_delay: float = 0.5, idempotent: bool = True) -> dict`:**
  - Chỉ retry `(RateLimitError, TimeoutError)` khi `idempotent=True`, tối đa `max_retries` lần retry (tổng cộng tối đa `max_retries + 1` lần thử).
  - Khi `idempotent=False`, chỉ gọi `fn()` tối đa một lần (không bao giờ retry thao tác có side effect — tác dụng phụ).
  - Giữa các lần retry (`attempt = 0, 1, ...`), gọi `clock.advance(base_delay * (2 ** attempt))` và cộng dồn vào `wait_seconds`.
  - Trả về `{"ok": bool, "value": Any, "error": str | None, "attempts": int, "wait_seconds": float}`.
- **`run_budgeted_agent(task, client, registry, ctx, clock, pricing, budget, tools=None, max_steps=5, max_retries=2) -> dict`:**
  - Khởi tạo `messages = [{"role": "user", "content": task}]`, `steps = 0`, `retries = 0`.
  - Ở mỗi bước (tối đa `max_steps` bước):
    1. Kiểm tra `reason = budget.check()`; nếu khác `None`, trả về ngay với `answer=None` và `stopped_reason=reason`.
    2. Gọi `call_with_retry(lambda: client.chat(messages, tools=tools), clock, max_retries=max_retries, idempotent=True)` và cộng `res["attempts"] - 1` vào `retries`. Nếu `not res["ok"]`, trả về `answer=None`, `stopped_reason="rate_limit"`.
    3. Tăng `steps += 1`, gọi `budget.record(resp.usage, pricing)` rồi kiểm tra `budget.check()` lần nữa; nếu khác `None`, trả về `answer=None` và `stopped_reason=reason`.
    4. Nếu `not resp.tool_calls`, trả về `answer=resp.content`, `stopped_reason="final"`.
    5. Ngược lại, thêm `{"role": "assistant", "content": resp.content or ""}` (bắt buộc có `"content"` dạng chuỗi cho `FakeLLM.chat`), thực thi mỗi tool call `tc` **đúng một lần** qua `registry.execute(tc.name, tc.arguments, ctx)` (không retry lệnh gọi tool), rồi thêm `{"role": "tool", "content": json.dumps(outcome, sort_keys=True)}`.
  - Nếu dùng hết `max_steps` mà chưa có câu trả lời cuối, trả về `answer=None`, `stopped_reason="max_steps"`.
  - Cấu trúc kết quả trả về: `{"answer": str | None, "stopped_reason": str, "steps": int, "total_tokens": int, "cost_usd": float, "retries": int}`.
