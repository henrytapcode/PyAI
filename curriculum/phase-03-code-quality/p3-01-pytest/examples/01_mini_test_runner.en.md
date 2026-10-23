# A tiny test runner

**What it shows:** how a tool like pytest works in spirit. It finds every function whose name starts with `test_`, calls it, and prints PASS or FAIL. One test is red on purpose because `clean_text` has a bug.

**Step by step**
1. Lines 2–4 define `clean_text` with a bug: `replace("  ", " ")` only turns two spaces into one, so three spaces become two.
2. Lines 7–17 define three tests. The last one has an assert message that shows what the function really returned.
3. Line 22 loops over `globals()`, a dict of every name defined so far. `list(...)` makes a copy first, because the loop itself adds the names `name` and `func`.
4. Lines 23–30 keep only names that start with `test_`, call each one inside `try`, and count passes and failures. A failed `assert` raises `AssertionError`, and `except` catches it so the other tests still run.
5. Line 32 prints the summary.

**Notice:** the failing test is the one with the longer run of spaces. The two easy tests passed, so the bug hid until a test looked at the edge.

**Try it yourself:** change the body of `clean_text` to `" ".join(text.split()).lower()` and run again. All three tests should pass.
