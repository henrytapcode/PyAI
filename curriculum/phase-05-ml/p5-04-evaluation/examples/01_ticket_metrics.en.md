# Imbalanced ticket evaluation

**What it shows:** Comparing a `DummyClassifier` baseline against a `LogisticRegression` pipeline on an 85/15 imbalanced dataset using accuracy, confusion matrix, precision, recall, F1, and `classification_report`.

**Step by step**
1. Lines 17–22 create 200 synthetic tickets with an 85/15 class balance and make a stratified 70/30 train/test split (`51` normal, `9` urgent in test).
2. Lines 24–28 fit both `DummyClassifier(strategy="most_frequent")` and a scaled `LogisticRegression` pipeline, then compute predictions on `X_test`.
3. Lines 30–36 compare baseline accuracy (`0.85`) and recall (`0.0` with `zero_division=0`) against the model's accuracy (`0.883`).
4. Lines 37–44 print the confusion matrix `[[51, 0], [7, 2]]`, precision/recall/F1 (`1.0`, `0.222`, `0.364`), and full `classification_report`.

**Notice:** Accuracy jumps from `0.85` to `0.883`, yet the confusion matrix reveals the model missed `7` of the `9` urgent tickets (`recall = 0.222`).

**Try it yourself:** Change `LogisticRegression()` to `DecisionTreeClassifier(max_depth=3, random_state=0)` (imported from `sklearn.tree`) and see how recall and precision shift.
