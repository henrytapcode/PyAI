# Pre-filter vs. post-filter

**What it shows:** Why applying a metadata filter *before* top-k ranking returns the requested `k` matches while filtering *after* top-k can drop to zero results.

**Step by step**
1. Lines 5–21 embed six bilingual records and the query `"money back for laptop"`, with `k = 2` and `where = {"lang": "vi"}`.
2. Lines 24–30 run **post-filter**: they pick the global top-2 (`d2` and `d1`, both English) and only then filter for `lang == "vi"`, leaving `0` hits.
3. Lines 33–39 run **pre-filter**: they slice `matrix[kept]` down to the three `"vi"` rows first and then pick top-2, returning `[('d4', 0.516), ('d5', 0.236)]`.

**Notice:** Both approaches see the exact same scores; only the order of filtering and slicing `[:k]` changes, turning `0` hits into the full `2` requested hits.

**Try it yourself:** Increase `k` to `4` in the post-filter step and check how many `"vi"` hits survive (`1` instead of `2`).
