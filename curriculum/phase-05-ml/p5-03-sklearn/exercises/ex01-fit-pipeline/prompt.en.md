Replace the `___` blanks in `train_and_score(X, y, seed)` so it creates a stratified 75/25 split, builds a `StandardScaler` + `LogisticRegression` pipeline, fits it on train, and returns the rounded test accuracy. Write your code inside the function and `return` the Python `float`.

**Example**

```python
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
score = train_and_score(X, y, seed=42)
# 0.921
```

**Rules**

- Use `train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)`.
- Build the pipeline with `make_pipeline(StandardScaler(), LogisticRegression())`.
- Fit the pipeline strictly on `(X_train, y_train)` and score on `(X_test, y_test)`.
- Return `round(float(score), 3)` as a plain Python `float`, without modifying `X` or `y`.
