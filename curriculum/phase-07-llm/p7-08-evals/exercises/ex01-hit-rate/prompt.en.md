Fill in the `___` blanks in `hit_rate(results, k)` inside `starter.py` to compute retrieval `hit@k` over answerable eval rows.

Write your code inside the function and `return` a `float` between `0.0` and `1.0`.

## Example

```python
results = [
    {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
    {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md"]},
    {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
]
hit_rate(results, k=1)  # -> 0.5
hit_rate(results, k=2)  # -> 1.0
```

## Rules

- Each element in `results` is `{"expected_source": str | None, "retrieved": list[str]}` ordered from highest score to lowest.
- Skip rows where `expected_source` is `None` so unanswerable questions are not included in the denominator.
- Count a row as a hit when `expected_source` appears inside `retrieved[:k]`.
- Return `0.0` when `results` has no rows with a non-`None` `expected_source` (or when `k <= 0`).
