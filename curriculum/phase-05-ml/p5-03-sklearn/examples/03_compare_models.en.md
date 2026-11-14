# Comparing three models fairly

**What it shows:** Running `LogisticRegression`, `KNeighborsClassifier`, and `DecisionTreeClassifier` through identical `StandardScaler` pipelines on one shared `iris` split as a first look at held-out performance.

**Step by step**
1. Lines 10–13 load the built-in `iris` dataset (150 flowers, 3 classes) and create one stratified 70/30 split with `random_state=42`.
2. Lines 15–19 define the three candidate estimators with explicit hyperparameters (`max_iter=1000`, `n_neighbors=5`, `max_depth=3` with `random_state=0`).
3. Lines 24–32 loop over each candidate, wrap it in `make_pipeline(StandardScaler(), estimator)`, fit on `X_train`, print both train and held-out accuracy, and track the highest score.
4. Line 34 prints the top candidate on this held-out split (`DecisionTree` at `0.933`).

**Notice:** All three pipelines tie at `0.981` on train, so train score cannot separate them; meanwhile, `DecisionTree` (`0.933`, 42/45) beats the other two (`0.911`, 41/45) by only 1 sample out of 45 — a tiny gap inside single-split luck, which is why `p5-04-evaluation` uses cross-validation on train to choose models reliably.

**Try it yourself:** Change `DecisionTreeClassifier(max_depth=3, ...)` to `max_depth=None` — the deeper tree memorizes train (`1.000`) and happens to score `0.978` (44/45) on this particular small test split, showing how noisy a single split can be compared with cross-validation.
