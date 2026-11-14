# Decision threshold tradeoff

**What it shows:** Sweeping five decision thresholds over `predict_proba` on a validation split carved from train to pick the highest threshold meeting `recall >= 0.8`, then evaluating the held-out test set once.

**Step by step**
1. Lines 10–18 build the 85/15 split (`train_full` / `test`) and split `train_full` again into `train` and `val` with `stratify` so threshold tuning never touches `test`.
2. Lines 20–25 fit the `LogisticRegression` pipeline on `X_train`, extract validation probabilities `.predict_proba(X_val)[:, 1]`, and set `target_recall = 0.8`.
3. Lines 27–35 sweep thresholds `0.5` down to `0.1` on `val`, print rounded precision, recall, and flagged count, and pick the largest threshold reaching `recall >= target_recall` (`0.3`).
4. Lines 37–45 print the chosen threshold (`0.3`) and, because one qualified, evaluate `X_test` once (`precision=0.875`, `recall=0.778`).

**Notice:** Dropping the threshold from `0.5` to `0.3` on validation boosts recall from `0.400` to `0.800` with precision at `0.667`; evaluating `t = 0.3` once on unseen `X_test` gives `precision=0.875` and `recall=0.778`.

**Try it yourself:** Raise `target_recall` on line 24 from `0.8` to `0.95` and see `best_threshold` become `None` because none of the five thresholds reaches `0.95` on validation.
