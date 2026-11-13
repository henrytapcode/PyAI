# Decision threshold tradeoff

**What it shows:** Sweeping five decision thresholds over `predict_proba` outputs to trade precision against recall and pick the highest threshold that reaches `recall >= 0.8`.

**Step by step**
1. Lines 11–19 build the 85/15 split, fit the `LogisticRegression` pipeline, and extract class-1 probabilities with `.predict_proba(X_test)[:, 1]`.
2. Lines 21–24 list five candidate thresholds (`0.5` down to `0.1`) and print the table header.
3. Lines 25–32 turn probabilities into `0/1` predictions for each threshold, compute rounded precision, recall, and flagged count, and keep the highest threshold meeting `recall >= 0.8`.
4. Line 34 prints the chosen threshold (`0.3`).

**Notice:** Dropping from `0.5` to `0.3` boosts recall from `0.222` to `0.889` while keeping precision at `0.889`; going lower to `0.1` adds false alarms (`17` flagged) with no extra recall gain.

**Try it yourself:** Raise the target in line 31 from `0.8` to `0.95` and see whether any of these five thresholds satisfies it.
