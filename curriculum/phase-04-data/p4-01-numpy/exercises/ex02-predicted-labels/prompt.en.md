A classifier outputs a 2D array `probs` where each row is a sample and each column is a class probability. Write `predicted_labels(probs, labels, threshold)` that picks the highest-probability class for each row, or `"unsure"` if that probability is below `threshold`. Write your code inside the function and `return` the answer as a Python `list` of strings.

**Example**

```python
probs = np.array([[0.10, 0.90], [0.55, 0.45]])
predicted_labels(probs, ["no", "yes"], 0.6)
# -> ["yes", "unsure"]
```

**Rules**
- Use `probs.argmax(axis=1)` (or row `argmax`) so ties pick the first matching class index.
- If the top probability equals `threshold` (`prob >= threshold`), accept the predicted label.
- Return a plain Python `list[str]`, not a NumPy array.
- Do not modify `probs` or `labels`.
