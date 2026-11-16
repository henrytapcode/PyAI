Complete `percentile` and `latency_report` in `starter.py` by replacing every `___` blank so they compute nearest-rank percentiles and return the summary dictionary. Keep the existing function signatures and validation check.

**Example**

```python
percentile([10, 20, 30, 40], 50)   # 20.0
latency_report([100, 200, 300])    # {"p50": 200.0, "p95": 300.0, "max": 300.0}
```

**Rules**
- `percentile(values, p)` sorts `values` without mutating the input, computes `rank = math.ceil(p / 100 * len(ordered))`, and returns `float(ordered[rank - 1])`.
- `percentile` raises `ValueError` when `values` is empty or when `p` is outside `(0, 100]`.
- `latency_report(values)` returns `{"p50": ..., "p95": ..., "max": ...}` with `float` values.
