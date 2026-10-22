# Converting form data

**What it shows:** why text from the outside world must be converted before you do maths with it.

**Step by step**
1. Lines 2–3 hold the values exactly as a web form would send them: as text, even though they look like numbers.
2. Line 5 adds two strings. `+` on text means "join", so you get `2121`, not `42`.
3. Lines 6–7 convert: `int()` for the whole number, `float()` for the decimal.
4. Line 8 adds two real numbers and prints `42`. Lines 9–10 use the converted values inside f-strings.
5. Line 11 proves the conversion worked: `<class 'int'> <class 'float'>`.

**Notice:** `1.68 * 100` prints `168.0`, not `168`. A float stays a float even when the result is a whole number.

**Try it yourself:** change line 6 to `age = int(height_text)` and run it. Read the `ValueError` message: it tells you exactly which text could not be converted.
