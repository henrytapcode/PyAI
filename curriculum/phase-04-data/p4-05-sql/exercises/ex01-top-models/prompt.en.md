Complete `top_models(conn, min_runs)` by filling in the `___` blanks in the SQL query over `runs(model TEXT, score REAL)`. Return a list of `(model, avg_score)` tuples for models with at least `min_runs` runs, rounded to 2 decimal places and sorted by highest `avg_score` first (and alphabetically by `model` on ties). Write your code inside the function and `return` the list of tuples.

**Example**

```python
# Table runs contains:
# ("gpt-4o", 0.92), ("gpt-4o", 0.88), ("claude", 0.88), ("claude", 0.88), ("mini", 0.95)
top_models(conn, 2)
# [("gpt-4o", 0.9), ("claude", 0.88)]
```

**Rules**

- Keep only models with `COUNT(*) >= min_runs`, using a `?` placeholder for `min_runs`.
- Round each average score to 2 decimal places using SQL `ROUND`.
- Order by `avg_score` descending, then `model` ascending to break ties.
