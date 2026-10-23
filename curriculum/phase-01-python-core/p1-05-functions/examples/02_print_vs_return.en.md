# print vs return

**What it shows:** two functions that look almost the same but behave very differently.

**Step by step**
1. Lines 2–3: `double_print` computes `n * 2` and **shows** it with `print`. It has no `return`, so it hands back `None`.
2. Lines 6–7: `double_return` computes the same number and **returns** it to whoever called it.
3. Line 10 calls `double_print(4)`. The screen shows `8` (that is the first output line), but the variable `a` receives `None`.
4. Line 11 calls `double_return(4)`. Nothing appears on screen, but `b` receives `8`.
5. Lines 12–14 print what `a` and `b` hold. Line 14 works because `b` is a real number: `8 + 1`. Try `a + 1` and you get a `TypeError`.

**Notice:** the `8` printed first comes from line 3 inside the function, not from the `print("a is", a)` line.

**Try it yourself:** change line 14 to `print("a + 1 =", a + 1)` and read the error message. Then change it back.
