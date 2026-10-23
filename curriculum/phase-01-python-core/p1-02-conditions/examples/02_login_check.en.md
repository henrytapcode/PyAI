# Login check

**What it shows:** `and`, `or`, `not` in real checks, and how empty text behaves inside an `if`.

**Step by step**
1. Lines 2–4 store a username, a password and the number of failed attempts so far.
2. Line 6 builds a `bool`: `username != ""` is `True` because `"lan"` is not empty. Line 7 does the same with `len(password) >= 8` (`len()` counts the characters; `"secret123"` has 9), which is `True`.
3. Line 9 uses `and`: both `has_name` and `long_password` are `True`, so line 10 prints `Credentials look valid`.
4. Line 12 uses `or` and `not`: `attempts >= 3` is `False` (2 is less than 3) and `not has_name` is `False` too. `False or False` is `False`, so the `else` runs and line 15 prints `1 attempt(s) left` (3 - 2 = 1).
5. Line 17 sets `nickname` to an empty string. Line 18 `if nickname:` treats `""` as False, so the `else` on line 20 runs and line 21 prints `Hi, stranger`.
6. Line 23 shows the same rule directly: `bool("")` is `False`, `bool("a")` is `True`, `bool(0)` is `False`, `bool(5)` is `True`.

**Notice:** `if nickname:` is a short way to write `if nickname != "":`. Both mean "has something in it".

**Try it yourself:** change `attempts` to `3` and predict which branch of the second `if` runs. Then change `password` to `"abc"` and see which line disappears.
