# Grade histogram

**What it shows:** counting with a dict, then turning the counts into a simple text chart. This is the same idea as the `grade_counts` in `class_stats`.

**Step by step**
1. Line 2 is a list of letters, as if `letter_grade` had already been run for seven students.
2. Line 4 creates the counting dict with every letter set to `0`. Having all five keys from the start means a letter nobody got still shows up as `0`.
3. Lines 5–6 loop over the letters. `counts[letter] += 1` finds the right key and adds one.
4. Line 8 prints the whole dict.
5. Lines 9–10 loop with `.items()`, which gives each key and value together. `'#' * how_many` repeats the `#` character that many times, which draws the bar.

**Notice:** if you started with an empty dict `{}`, then `counts["A"] += 1` would crash with a `KeyError` the first time, because the key does not exist yet. Starting with all five keys avoids that.

**Try it yourself:** add `"D"` to the list and run again. Predict the new `D` line before you run it (it should be `D: # (1)`).
