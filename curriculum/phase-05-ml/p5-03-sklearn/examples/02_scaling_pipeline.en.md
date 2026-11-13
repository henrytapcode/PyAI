# Feature scaling inside a Pipeline

**What it shows:** Why `KNeighborsClassifier` fails when one feature (`tokens`, 200–4000) dwarfs another (`error_rate`, 0.0–0.45), and how `make_pipeline(StandardScaler(), ...)` fixes it without data leakage.

**Step by step**
1. Lines 8–12 build 40 rows where `tokens` is noisy on a large scale while `error_rate` cleanly separates class `0` from class `1` on a tiny `[0, 0.45]` scale.
2. Lines 14–16 split the data once with `random_state=42` and `stratify=y`.
3. Lines 18–20 fit a plain `KNeighborsClassifier(n_neighbors=3)` on unscaled features (`0.5` test accuracy — no better than a coin flip).
4. Lines 22–24 wrap `StandardScaler()` and `KNeighborsClassifier(n_neighbors=3)` in `make_pipeline`, which learns the scaling stats strictly from `X_train` and reuses them on `X_test`.

**Notice:** Without scaling, differences of hundreds of tokens completely drown out differences of `0.1` in `error_rate` when KNN measures distance.

**Try it yourself:** Change `n_neighbors=3` to `1` or `5` in both models and check whether unscaled KNN ever catches up to the pipeline.
