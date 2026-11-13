# Tuning the threshold on train CV and writing an honest report

**What it shows:** Picking the decision threshold strictly from training out-of-fold probabilities (`cross_val_predict`), evaluating the untouched test split once, and printing a multi-line report with sample size, baseline, CV spread, and a statistical tie warning.

**Step by step**
1. Lines 56–66 select `logreg` and `tree` CV F1 scores on `X_train`, then use `cross_val_predict(..., method="predict_proba")` on `X_train` to pick the highest threshold in `[0.5, 0.4, 0.3, 0.2]` reaching `recall >= 0.80` (`0.2`).
2. Lines 68–71 fit `DummyClassifier` and `logreg` on all `173` training rows and score the `58` holdout test rows once using threshold `0.2`.
3. Lines 73–86 print the honest report: test sample size (`58`, `14` urgent), baseline (`acc=0.759 F1=0.000`), CV `mean +/- std` for both models, test confusion matrix `[[31, 13], [1, 13]]`, test precision/recall/F1, and the tie caveat.

**Notice:** Choosing the threshold on `X_train` keeps `X_test` completely unseen until the single final check (`13` of `14` urgent tickets caught, `recall=0.929`).

**Try it yourself:** Raise the training OOF recall target from `0.80` to `0.90` on line 64 and observe what happens to `chosen_t` and test precision.
