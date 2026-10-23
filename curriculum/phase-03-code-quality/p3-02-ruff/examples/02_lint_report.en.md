# Summarize a lint report

**What it shows:** CI scripts often read the short form of ruff's output. This program parses six report lines and counts the problems by rule code and by file.

**Step by step**
1. Lines 2–9 store the report. Each line is `file:line:column: CODE message`.
2. Lines 12–15 split one line on `:` into four parts, then split the last part into words. The first word is the rule code, and `"[*]" in words` is `True` when ruff can fix the problem.
3. Lines 18–26 loop over the report. `by_code.get(code, 0) + 1` is the counting pattern: start from `0` the first time a code appears.
4. Lines 28–34 print the counts in sorted order, then how many of the six problems `--fix` could repair.

**Notice:** the variables that hold the line number and the column start with `_`. That is the habit for "I unpack this value but I do not need it", and it keeps tools quiet about unused names.

**Try it yourself:** add `"util.py:12:1: F401 [*] `re` imported but unused"` to `REPORT`. `F401` should now show `3`, and `fixable` should be `3 of 7`.
