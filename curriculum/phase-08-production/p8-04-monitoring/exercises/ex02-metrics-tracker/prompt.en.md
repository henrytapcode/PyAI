Implement `MetricsTracker` in `starter.py` to record per-request latency, token cost, and status, aggregate them in `summary()`, and evaluate threshold rules in `alerts()`. Write your code inside the class methods and return the requested values.

**Example**

```python
tracker = MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
cost = tracker.record(latency_ms=250.0, prompt_tokens=1000, completion_tokens=500)
# cost == 0.002
tracker.summary()
# {"count": 1, "error_rate": 0.0, "p95_ms": 250.0, "total_cost": 0.002}
tracker.alerts(max_p95_ms=200.0, budget=0.0025)
# ["p95-latency", "budget-warning"]
```

**Rules**
- `record(latency_ms, prompt_tokens, completion_tokens, ok=True)` stores the request (even when `ok=False`) and returns its cost as a `float`.
- `summary()` returns `{"count": ..., "error_rate": ..., "p95_ms": ..., "total_cost": ...}` using nearest-rank `p95_ms` and `round(total_cost, 6)`. When no requests have been recorded, `count` is `0` and all other values are `0.0`.
- `alerts(max_p95_ms, budget, warn_ratio=0.8)` returns alert code strings in fixed order:
  1. `"p95-latency"` if `p95_ms > max_p95_ms`
  2. `"budget-exceeded"` if `total_cost > budget`, otherwise `"budget-warning"` if `total_cost >= warn_ratio * budget`
  3. `"error-rate"` if `error_rate > 0.05`
