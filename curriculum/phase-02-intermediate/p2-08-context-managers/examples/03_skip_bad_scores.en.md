# Skip bad scores

**What it shows:** a manager that hides one kind of error and counts how many it hid, used to clean messy data.

**Step by step**
1. Lines 3–5 store which error type to hide and start a counter at 0.
2. Lines 7–8 are `__enter__`: it returns `self`.
3. Lines 10–14 are `__exit__`: if the error is the expected type, count it and return `True` (hide it); otherwise return `False` (let it through).
4. Lines 17–23 go through the raw text. The same manager `skip` is reused in every loop turn. A bad value such as `"n/a"` raises `ValueError`, which is hidden, and the loop continues.
5. Lines 28–32 try `float(None)`. That raises `TypeError`, which is a different type, so it is not hidden and `except` catches it.

**Notice:** the counter stays at 2 after the `TypeError`, because `__exit__` returned `False` for it.

**Try it yourself:** change `SkipErrors(ValueError)` on line 19 to `SkipErrors(TypeError)`. The first loop now crashes on `"n/a"`, because `ValueError` is no longer hidden.
