# Stratified cross-validation across three models

**What it shows:** Comparing three classifiers (`LogisticRegression`, `KNeighborsClassifier`, and `DecisionTreeClassifier`) on `load_breast_cancer` using 5-fold `StratifiedKFold` and F1 scoring inside `make_pipeline`.

**Step by step**
1. Lines 12–13 load the built-in 569-row breast cancer dataset (`[212, 357]` class counts).
2. Lines 15–20 set up a reproducible 5-fold `StratifiedKFold` splitter and three candidate estimators.
3. Lines 25–33 wrap each candidate in `make_pipeline(StandardScaler(), estimator)`, evaluate 5-fold `cross_val_score(..., scoring="f1")`, and print `mean` and `std` rounded to 3 decimals.
4. Line 35 reports the winner (`LogReg` with F1 `0.983`).

**Notice:** Placing `StandardScaler()` inside `make_pipeline` guarantees each of the 5 folds fits scaling strictly on its own 4 training folds, preventing leakage across folds.

**Try it yourself:** Change `scoring="f1"` in line 27 to `scoring="recall"` and check whether the ranking or spread changes.
