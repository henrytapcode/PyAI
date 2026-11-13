The starter code defines `slow_requests(df, limit_ms)`, which tries to return every API request slower than `limit_ms`, keeping only the `["endpoint", "latency_ms"]` columns, sorted slowest-first with a clean `0, 1, ...` index. It runs without crashing, but it has **three bugs** — fix them inside the function and `return` the resulting DataFrame.

**Example**

```python
df = pd.DataFrame({
    "endpoint": ["/chat", "/health", "/embed"],
    "latency_ms": [200, 350, 520],
    "status": [200, 200, 500],
})
slow_requests(df, 200)
#   endpoint  latency_ms
# 0   /embed         520
# 1  /health         350
```

**Rules**
- Keep only rows with `latency_ms` **strictly greater than** `limit_ms`.
- Return only the columns `["endpoint", "latency_ms"]` in that order.
- Sort by `latency_ms` descending (largest first) and reset the index (`0, 1, ...`) without adding an `"index"` column.
- Do not modify the input `df`.
