# A table of cases

**What it shows:** the idea behind `parametrize`. Instead of one test per input, you write a table of `(input, expected)` pairs and run the same check on every row, then report which rows failed.

**Step by step**
1. Lines 2–3 are the function under test, `normalize_spaces`.
2. Lines 6–12 are the table. Each row is one case: a normal text, tabs and newlines, an empty text, only spaces, and a plain word.
3. Lines 14–21 run every row. A row that matches adds one to `passed`; a row that does not is saved with its text, expectation and result.
4. Lines 23–25 print the failures first and then the totals.

**Notice:** the last row fails, but the function is right. The expectation `"one "` has a space that the function correctly removes. A red test means "look here", and the bug can be in the test. Read both sides before you change anything.

**Try it yourself:** fix the last row to `("one", "one")`. The report should say `5 passed, 0 failed`.
