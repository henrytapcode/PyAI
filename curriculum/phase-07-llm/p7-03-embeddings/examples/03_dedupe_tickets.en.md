# Finding near-duplicate support tickets

**What it shows:** Computing all pairwise cosine similarities at once with `matrix @ matrix.T` and scanning only the upper triangle to detect duplicate tickets.

**Step by step**
1. Lines 5–13 list five support `TICKETS` and set `THRESHOLD = 0.5`.
2. Lines 15–17 embed all five tickets once into `matrix` (shape `(5, 256)`) and multiply `matrix @ matrix.T` to get a `5 x 5` similarity grid.
3. Lines 20–25 loop over `i` and `j > i` (the upper triangle) so each pair is checked once and self-pairs `(i, i)` are skipped.
4. Lines 23–25 print every pair whose cosine meets or exceeds `THRESHOLD`.

**Notice:** Looping `j` from `i + 1` avoids checking both `(0, 1)` and `(1, 0)` as well as trivial self-matches `(0, 0)` where cosine is always `1.0`.

**Try it yourself:** Lower `THRESHOLD` to `0.3` or add a ticket `"My laptop has a startup failure"` and observe the new duplicate pairs.
