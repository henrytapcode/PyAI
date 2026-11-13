# Row-by-row loop with itertuples

This approach iterates over `df.itertuples(index=False)` and keeps running sums and counts in two Python dicts, returning `{}` naturally when no `"ok"` rows match. While the accumulator logic is familiar from Phase 1, pandas `.groupby("model")["score"].mean()` is much shorter to write and significantly faster on large tables because the grouping and averaging run inside compiled code rather than a Python loop.
