Fill in the `___` blanks in `hit_rates(results, ks)` inside `starter.py` to compute retrieval `hit@k` across multiple cutoffs `ks`.

Write your code inside the function and `return` a `dict[int, float]` mapping each `k` in `ks` to its score rounded to 3 decimal places.

## Example

```python
results = [
    {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
    {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md"]},
    {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
]
hit_rates(results, ks=[1, 2])  # -> {1: 0.5, 2: 1.0}
```

## Rules

- Each element in `results` is `{"expected_source": str | None, "retrieved": list[str]}` ordered from highest score to lowest.
- Raise `ValueError` if any `k` in `ks` is `<= 0`.
- Skip rows where `expected_source` is `None` so unanswerable questions stay out of the denominator; return `{}` when `ks` is empty.
- Count a row as a hit when `expected_source` appears inside `retrieved[:k]`, and store `round(hits / total, 3)` (or `0.0` when no answerable rows exist).
