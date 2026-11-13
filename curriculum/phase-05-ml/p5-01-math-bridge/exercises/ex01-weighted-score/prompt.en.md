Replace the `___` blanks in `weighted_score(features, weights, bias)` so it computes the weighted score of a feature vector and returns it as a Python `float`. Write your code inside the function and `return` the answer.

**Example**

```python
weighted_score(np.array([2.0, 3.0]), np.array([0.5, 1.0]), 0.5)  # 4.5
```

**Rules**

- Combine `features` and `weights` using the dot product, then add `bias`.
- Return a built-in Python `float` (`type(result) is float`), not a NumPy scalar.
- Do not modify `features` or `weights` in place.
