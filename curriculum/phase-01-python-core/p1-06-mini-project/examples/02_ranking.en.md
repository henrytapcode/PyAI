# Ranking students

**What it shows:** how to rank a list of dicts with `sorted(..., key=...)` and a tuple key, including what happens when two students tie.

**Step by step**
1. Lines 2–5 are the same `average` you already know.
2. Lines 8–9 define `sort_key`. It receives one row and returns the tuple `(-avg, name)`. The minus sign flips the order, so the highest average comes first.
3. Lines 12–17 hold the raw data. Mai and Zoe both end up with an average of `7.0`.
4. Lines 19–21 turn each student into a small row `{"name": ..., "avg": ...}`. Sorting is easier on rows that already contain the average, because we compute it only once.
5. Line 24 sorts the rows. `key=sort_key` has **no parentheses**: we pass the function itself, and Python calls it on every row.
6. Lines 23–26 print a numbered list. `rank` starts at 1 and goes up by 1 after each line.

**Notice:** Mai and Zoe have the same average, so Python compares the second value of the tuple, the name. `"Mai"` comes before `"Zoe"` alphabetically, so Mai is listed first.

**Try it yourself:** change Zoe's scores to `[10, 10]`. Predict who is rank 1 now (Zoe, with `10.00`).
