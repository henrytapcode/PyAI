Complete `confusion_counts(y_true, y_pred)` by replacing every `___` blank so it counts True Positives, False Positives, False Negatives, and True Negatives for binary `0`/`1` arrays. Write your code inside the function and `return` the dictionary of plain Python `int` counts.

**Example**

```python
y_true = np.array([1, 1, 0, 0])
y_pred = np.array([1, 0, 1, 0])
confusion_counts(y_true, y_pred)
# {'tp': 1, 'fp': 1, 'fn': 1, 'tn': 1}
```

**Rules**
- Replace every `___` blank using NumPy boolean comparisons (`&`) and `.sum()`.
- Convert every count to a plain Python `int` (not a NumPy scalar).
- Return keys `"tp"`, `"fp"`, `"fn"`, `"tn"` in a dictionary without modifying `y_true` or `y_pred`.
