# Eval scores by model

**What it shows:** grouping rows by model with `groupby`, computing mean and count with `.agg(...)`, and picking the top model.

**Step by step**
1. Lines 4–8 build an `evals` DataFrame with scores for three models across two tasks (`qa` and `code`).
2. Line 10 groups by `"model"`, computes both `"mean"` and `"count"` on `"score"`, and rounds to 2 decimals.
3. Line 11 sorts the grouped table from highest mean score to lowest.
4. Lines 14–16 read the winning model name from `summary.index[0]` and its score from `summary.iloc[0]["mean"]`.

**Notice:** after `groupby("model")`, the model names become the DataFrame's **index**, which is why `summary.index[0]` gives `"claude"` and `summary.iloc[0]["mean"]` reads row `0`'s mean score.

**Try it yourself:** lower `claude`'s `"code"` score on line 7 from `0.94` to `0.80` and watch `gpt-4o` move into first place (`0.9` vs `0.84`).
