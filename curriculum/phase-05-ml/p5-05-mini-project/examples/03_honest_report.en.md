# Tuning the threshold on train CV and writing an honest report

**What it shows:** Picking the decision threshold strictly from training out-of-fold probabilities (`cross_val_predict`), evaluating the untouched test split once, and printing a multi-line report with sample size, baseline, CV spread, and a statistical tie warning.

**Step by step**
1. Lines 54–68 compute 5-fold CV F1 scores for `logreg` and `tree` on `X_train`, then use `cross_val_predict(..., method="predict_proba")` on `X_train` to pick the highest threshold in `[0.5, 0.4, 0.3, 0.2]` reaching `target_recall` (`0.80` on line 62, yielding `0.2`), leaving `chosen_t = None` if none qualifies.
2. Lines 70–78 fit `DummyClassifier` on the `173` training rows and print the test sample size (`58`, `14` urgent), baseline (`acc=0.759 F1=0.000`), and CV `mean +/- std` for both models.
3. Lines 79–92 print `"no threshold reaches recall >= ..."` and skip test evaluation when `chosen_t is None`; otherwise they fit `logreg` on `X_train`, score the `58` holdout test rows once at `0.2`, print confusion matrix `[[31, 13], [1, 13]]`, test precision/recall/F1, and the tie caveat.

**Notice:** Choosing the threshold on `X_train` keeps `X_test` completely unseen until the single final check (`13` of `14` urgent tickets caught, `recall=0.929`).

**Try it yourself:** Raise `target_recall` from `0.80` to `0.90` on line 62 and observe that no threshold in `[0.5, 0.4, 0.3, 0.2]` qualifies (`chosen_t = None`), so it prints `"no threshold reaches recall >= 0.90"` instead of scoring `X_test`.
