# Score statistics

**What it shows:** the everyday list toolkit on one list: `append`, indexing, slicing, a `for` loop with an accumulator, `sorted` and `in`.

**Step by step**
1. Line 2 creates a list of three model scores. Line 3 adds a fourth with `.append`, so the list now has 4 items.
2. Line 5 prints `len(scores)`, which is `4`. Line 6 prints the first item (`scores[0]`) and the last one (`scores[-1]`).
3. Line 7 takes a slice from index 1 up to, but not including, index 3. That is the 2nd and 3rd items: `[0.91, 0.78]`.
4. Lines 9–11 are the accumulator pattern: `total` starts at `0` and every score is added to it.
5. Lines 12–13 divide by the number of scores to get the average, then `round(average, 3)` keeps 3 decimals.
6. Line 14 prints a sorted copy. The original `scores` is not changed. Line 15 asks whether `0.91` is in the list: `True`.

**Notice:** the slice `scores[1:3]` has only 2 items, not 3. The `stop` index is never included.

**Try it yourself:** change line 7 to `scores[:2]` and predict the output before you run it (the first two scores: `[0.82, 0.91]`).
