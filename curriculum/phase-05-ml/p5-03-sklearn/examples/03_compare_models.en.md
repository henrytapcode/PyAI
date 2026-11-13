# Comparing three models fairly

**What it shows:** Running `LogisticRegression`, `KNeighborsClassifier`, and `DecisionTreeClassifier` through identical `StandardScaler` pipelines on one shared `iris` train/test split and selecting the winner by test score.

**Step by step**
1. Lines 10–13 load the built-in `iris` dataset (150 flowers, 3 classes) and create one stratified 70/30 split with `random_state=42`.
2. Lines 15–19 define the three candidate estimators with explicit hyperparameters (`max_iter=1000`, `n_neighbors=5`, `max_depth=3` with `random_state=0`).
3. Lines 24–32 loop over each candidate, wrap it in `make_pipeline(StandardScaler(), estimator)`, fit on `X_train`, print both train and test accuracy, and track the highest test score.
4. Line 34 announces `DecisionTree` (`0.933`) as the winner on the test set.

**Notice:** All three pipelines tie at `0.981` on train, so looking only at training accuracy could never tell them apart — only the held-out test set separates them.

**Try it yourself:** Change `DecisionTreeClassifier(max_depth=3, ...)` to `max_depth=None` and see whether the deeper tree wins or overfits on the test split.
