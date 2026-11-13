Replace the `___` blanks in `split_data(X, y, test_ratio, seed)` so it shuffles row indices reproducibly and returns `(X_train, X_test, y_train, y_test)`. Write your code inside the function and `return` the four arrays.

**Example**

```python
X = np.arange(10).reshape(5, 2)
y = np.arange(5)
X_train, X_test, y_train, y_test = split_data(X, y, test_ratio=0.2, seed=42)
# len(X_train) == 4, len(X_test) == 1, len(y_train) == 4, len(y_test) == 1
```

**Rules**

- Seed NumPy with `np.random.default_rng(seed)` and shuffle positions using `rng.permutation(len(X))`.
- Set `n_test = int(round(len(X) * test_ratio))`.
- Take the **first** `n_test` indices of `idx` for the test set and the remaining indices for the train set.
- Keep `X` and `y` aligned row for row, and do not modify the input arrays in place.
