# Encoding `plan` with boolean masks and `np.column_stack`

Instead of adding a `plan_code` column via `Series.map`, this approach filters to known plans first (`df["plan"].isin(...)`), encodes `"pro"` and `"enterprise"` directly as `0.0 / 1.0 / 2.0` using boolean masks, and assembles `X` with `np.column_stack`. Filtering early avoids extra DataFrame columns and makes missing-plan rows explicit, whereas `Series.map` in `solution.py` scales better when a category has many levels and keeps all feature columns inspectable in one table before converting to NumPy.
