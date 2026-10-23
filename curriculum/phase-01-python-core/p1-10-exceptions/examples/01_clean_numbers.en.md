# Cleaning messy numbers

**What it shows:** a small reusable helper, `safe_int`, that turns text into a number or gives back a default instead of crashing.

**Step by step**
1. Lines 2–6 define `safe_int`. The risky call `int(text)` is the only line inside `try`.
2. Line 5 catches two exception types at once. `"twelve"` and `""` raise `ValueError`; `None` raises `TypeError` (`int(None)` makes no sense).
3. Line 9 is the messy input. Note that `" 7 "` is fine: `int()` ignores spaces around the digits.
4. Line 14 asks for `default=None`. `None` can never be confused with a real number, so line 15 can ask `value is None` to spot failures.
5. Lines 16 and 18 count the bad values and collect the good ones. The program finishes with `sum: 59` instead of dying on the third value.

**Notice:** the default is a choice you make for each situation. `0` is fine when you only want a total; `None` is better when you must know that something went wrong.

**Try it yourself:** add `"3.5"` to `raw_values`. Is it counted as bad? (Yes: `int("3.5")` raises `ValueError`, so `bad values` becomes `4`.)
