Implement two evaluation functions from scratch without calling `sklearn.metrics`:

1. `precision_recall_f1(y_true, y_pred)` computes precision, recall, and F1 from the confusion counts (`tp`, `fp`, `fn`), returning `(0.0, ...)` for any metric whose denominator is zero, and rounding only at the end to 3 decimal places.
2. `threshold_for_recall(probs, y_true, thresholds, min_recall)` predicts `1` wherever `probs >= t` and returns the **largest** threshold in `thresholds` whose recall is at least `min_recall`, or `None` if no threshold qualifies.

Write your code inside both functions and `return` the answer.

**Example**

```python
precision_recall_f1(np.array([1, 1, 1, 0, 0]), np.array([1, 0, 0, 0, 0]))
# (1.0, 0.333, 0.5)

threshold_for_recall(
    np.array([0.8, 0.4, 0.2]),
    np.array([1, 1, 0]),
    thresholds=[0.3, 0.5, 0.7],
    min_recall=0.8,
)
# 0.3
```

**Rules**
- In `precision_recall_f1`, compute F1 from unrounded precision and recall (`0.0` when `precision + recall == 0`), then return a tuple of three plain Python `float` values rounded to 3 decimals.
- Do not call `sklearn.metrics` in `precision_recall_f1` or `threshold_for_recall`.
- `thresholds` may be in any order; return the largest qualifying threshold as a Python `float`, or `None` if none reaches `min_recall`.
- Do not modify the input arrays or `thresholds` list.
