Write two functions—`evaluate_models(X, y, seed)` and `write_report(results, n_test)`—to compare candidate classifiers with 5-fold stratified CV and format an honest summary report. Write your code inside each function and `return` its result.

**Example**

```python
results = {"baseline": (0.0, 0.0), "logreg": (0.709, 0.092), "tree": (0.701, 0.14)}
write_report(results, n_test=58)
```

Returns:

```text
[
    "baseline F1: 0.000 +/- 0.000",
    "logreg F1: 0.709 +/- 0.092",
    "tree F1: 0.701 +/- 0.140",
    "best: logreg",
    "test size: 58",
    "warning: logreg and tree differ by less than one std",
]
```

**Rules**

- `evaluate_models(X, y, seed)`:
  - Run 5-fold `StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)` across **all** rows of `X, y` (assuming the caller already held out the test split).
  - Evaluate these exact three models in order:
    - `"baseline"`: `DummyClassifier(strategy="most_frequent")`
    - `"logreg"`: `make_pipeline(StandardScaler(), LogisticRegression())`
    - `"tree"`: `DecisionTreeClassifier(max_depth=3, random_state=0)`
  - Score F1 with `make_scorer(f1_score, zero_division=0)` (or an equivalent warning-free method) so a `0.0` baseline score produces zero warnings.
  - Return `{name: (mean, std)}` with both numbers rounded to `3` decimal places as plain Python `float`s. Do not modify `X` or `y`.
- `write_report(results, n_test)`:
  - Raise `ValueError` if `results` has no non-baseline models (e.g., empty or only `"baseline"`).
  - Format one line per model in the exact order of `results`: `f"{name} F1: {mean:.3f} +/- {std:.3f}"`.
  - Append `f"best: {best_name}"` for the non-baseline model with the highest `mean` (break ties alphabetically by model name).
  - Append `f"test size: {n_test}"`.
  - If there are at least two non-baseline models, let `a` be the best non-baseline model and `b` be the second-best (ranked by highest `mean`, ties broken alphabetically). When `abs(mean_a - mean_b) < max(std_a, std_b)` (strict `<`), append `f"warning: {a} and {b} differ by less than one std"`.
  - Do not modify `results`.
