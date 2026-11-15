Implement two helper functions for calling an LLM reliably and estimating request cost:

1. `ask_with_retry(client, messages, max_attempts=3) -> tuple[str, int]`: call `client.chat(messages)` up to `max_attempts` times. Return `(content, attempts_used)` on success. Catch `RateLimitError` and retry until `max_attempts` is reached, then re-raise `RateLimitError`. Do not retry any other exception (such as `ValueError`).
2. `estimate_cost(usage, price_in_per_m, price_out_per_m) -> float`: compute the USD cost from `usage.prompt_tokens` and `usage.completion_tokens` using the given per-1M-token prices, rounded to 6 decimal places.

Write your code inside each function and `return` the answer.

**Example**

```python
client = FakeLLM(fail_times=2)
content, attempts = ask_with_retry(client, [{"role": "user", "content": "What is RAG?"}], max_attempts=3)
# attempts == 3

cost = estimate_cost(Usage(prompt_tokens=1000, completion_tokens=500, total_tokens=1500), 0.50, 1.50)
# 0.00125
```

**Rules**

- Only catch and retry `RateLimitError`; let `ValueError` and other exceptions fail immediately on attempt 1.
- Do not call `time.sleep()`.
- `estimate_cost` must return a built-in Python `float` rounded to 6 decimal places.
