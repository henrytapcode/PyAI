# Model selection with 5-fold stratified cross-validation

**What it shows:** Cleaning raw ticket logs, holding out 25% of the data as a test set, and comparing a `DummyClassifier` baseline, a `LogisticRegression` pipeline, and a `DecisionTreeClassifier` on the training split using 5-fold stratified F1.

**Step by step**
1. Lines 35–42 clean `plan` and `tokens`, drop duplicate `ticket_id` rows (`keep="first"`), encode `plan` to `0.0/1.0/2.0`, and drop rows missing numeric fields while excluding `escalated_to_oncall`.
2. Lines 44–47 build `X` and `y` (`231` clean rows) and create a stratified `75/25` split (`173` train, `58` test).
3. Lines 49–55 configure `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` and `make_scorer(f1_score, zero_division=0)` so the all-zero baseline scores `0.000` without warnings.
4. Lines 58–66 run `cross_val_score` strictly on `(X_train, y_train)` and print each model's CV F1 `mean` and `std`, selecting `logreg` (`0.709 +/- 0.092` vs `0.701 +/- 0.140`).

**Notice:** `logreg` (`0.709`) and `tree` (`0.701`) both beat `baseline` (`0.000`), yet their gap (`0.008`) is much smaller than their fold-to-fold `std` (`0.092` and `0.140`).

**Try it yourself:** Change `DecisionTreeClassifier(max_depth=3, random_state=0)` to `max_depth=5` and see whether CV F1 improves or its `std` widens.
