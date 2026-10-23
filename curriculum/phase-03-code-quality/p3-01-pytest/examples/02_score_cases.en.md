# A table of score cases

**What it shows:** the idea behind `parametrize`: one table of inputs and expected results, and one loop that checks every row. Valid scores are compared as floats with a small tolerance, and invalid ones must raise `ValueError`.

**Step by step**
1. Lines 2–6 define `parse_score`. It raises `ValueError` unless the text has exactly one `/`.
2. Lines 9–16 define `error_name`, which returns the name of the error a call raises, or `"no error"`.
3. Lines 19–20 hold the cases: `VALID` pairs of text and expected number, and `INVALID` texts that must be refused.
4. Lines 23–29 check each valid case with `abs(result - expected) < 1e-3` instead of `==`.
5. Lines 31–37 check that each invalid text raises `ValueError`.
6. Line 39 prints how many cases were fine.

**Notice:** the second-to-last line of the output is `FAIL 8/0`. Dividing by zero raises `ZeroDivisionError`, not `ValueError`. The table found a gap the author did not think about.

**Try it yourself:** fix `parse_score` so `"8/0"` raises `ValueError` (check the second number before dividing), then run again. The table should go all green.
