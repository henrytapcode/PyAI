Implement `accuracy(preds, labels)` and `best_threshold(scores, labels)` to evaluate and select a single-threshold binary classifier. Write your code inside the functions and `return` the answers.

**Example**

```python
scores = np.array([0.1, 0.4, 0.7, 0.9])
labels = np.array([0, 0, 1, 1])
accuracy(np.array([0, 1, 1, 1]), labels)  # 0.75
best_threshold(scores, labels)            # (0.7, 1.0)
```

**Rules**

- `accuracy(preds, labels)` returns the fraction `preds == labels` as a Python `float`, or `0.0` if `preds` is empty.
- `best_threshold(scores, labels)` tries each distinct value in `scores` as a threshold `t`, predicting `1` when `score >= t` and `0` otherwise.
- Return `(best_t, best_acc)` as built-in Python `float` values (`type(...) is float`), with `best_acc` rounded to 3 decimal places.
- When two thresholds tie for the highest accuracy, return the **smallest** `t`.
- If `scores` is empty, `best_threshold(scores, labels)` returns `(0.0, 0.0)`.
- Do not modify `preds`, `scores`, or `labels` in place.
