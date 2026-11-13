Write `average_score_by_model(df)` to compute the mean evaluation score for each model across successful runs (`status == "ok"`). Write your code inside the function and `return` the answer as a Python `dict[str, float]`.

**Example**

```python
df = pd.DataFrame({
    "model": ["gpt-4o", "gpt-4o", "claude", "llama"],
    "status": ["ok", "ok", "error", "ok"],
    "score": [0.90, 0.96, 0.0, 0.80],
})
average_score_by_model(df)
# -> {"gpt-4o": 0.93, "llama": 0.8}
```

**Rules**
- Keep only rows where `status == "ok"`. Models with zero `"ok"` rows must not appear in the returned dictionary.
- Round each average score to 2 decimal places.
- Return a plain Python `dict` whose values are plain Python `float` objects (not `np.float64`).
- Return `{}` when no rows have `status == "ok"` (or when `df` is empty).
- Do not modify the input `df`.
