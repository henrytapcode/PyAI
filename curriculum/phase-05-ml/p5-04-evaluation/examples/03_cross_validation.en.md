# Stratified cross-validation across three models

**What it shows:** Comparing three classifiers (`LogisticRegression`, `KNeighborsClassifier`, and `DecisionTreeClassifier`) on `load_breast_cancer` (flipped so `1` = malignant) using 5-fold `StratifiedKFold` and F1 scoring inside `make_pipeline`.

**Step by step**
1. Lines 12–15 load the built-in 569-row breast cancer dataset and flip `y = 1 - y` so class `1` represents malignant cases (212 malignant, 357 benign).
2. Lines 17–22 set up a reproducible 5-fold `StratifiedKFold` splitter and three candidate estimators.
3. Lines 27–35 wrap each candidate in `make_pipeline(StandardScaler(), estimator)`, evaluate 5-fold `cross_val_score(..., scoring="f1")`, and print `mean` and `std` rounded to 3 decimals.
4. Line 37 reports the winner (`LogReg` with F1 `0.971`).

**Notice:** Flipping `y = 1 - y` ensures F1 measures detection of malignant tumors rather than benign ones, and placing `StandardScaler()` inside `make_pipeline` guarantees each of the 5 folds fits scaling strictly on its own 4 training folds.

**Try it yourself:** Change `scoring="f1"` on line 29 to `scoring="recall"` — because `1` is malignant, recall now shows what fraction of real cancer cases each model catches (`LogReg` reaches `0.958`).
