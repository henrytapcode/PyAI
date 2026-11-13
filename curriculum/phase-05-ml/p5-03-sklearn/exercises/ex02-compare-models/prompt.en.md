Write two functions to compare candidate scikit-learn models on one shared split and pick the winner. Write your code inside each function and `return` the answer.

1. `compare_models(X, y, models, seed)`: make **one** stratified 70/30 split with `random_state=seed`, fit a fresh clone of each estimator in `models` on `(X_train, y_train)`, and return a `dict[str, float]` mapping each model name (in the same key order) to its test accuracy rounded to 3 decimals.
2. `best_model(scores)`: return the model name with the highest score; on a tie, return the name that comes first alphabetically; raise `ValueError` if `scores` is empty.

**Example**

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
)
models = {
    "logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "knn": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3)),
    "tree": DecisionTreeClassifier(max_depth=3, random_state=0),
}
scores = compare_models(X, y, models, seed=42)
# {'logreg': 0.722, 'knn': 0.833, 'tree': 0.722}
best_model(scores)
# 'knn'
```

**Rules**

- Split `(X, y)` **once** using `train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)`.
- Clone every estimator with `sklearn.base.clone(model)` before calling `.fit(...)` so the objects passed in `models` remain unfitted.
- Return Python `float` scores rounded to 3 decimal places, preserving the key order of `models`.
- In `best_model(scores)`, raise `ValueError` when `scores` is empty and break ties alphabetically (`"alpha"` beats `"zeta"`).
