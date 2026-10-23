# Weather advice

**What it shows:** an `if` / `elif` / `else` chain where the first matching branch wins, plus a separate `if` / `else` on a `bool`.

**Step by step**
1. Lines 2–3 store the inputs: `temperature` (an `int`) and `is_raining` (a `bool`).
2. Line 5 asks `31 >= 35`. That is `False`, so Python skips line 6 and moves to the next `elif`.
3. Line 7 asks `31 >= 25`. That is `True`, so line 8 runs and `advice` becomes `"Warm day"`. Lines 9–12 are skipped completely, even though `31 >= 15` is also true.
4. Line 14 prints the result with an f-string: `31 degrees: Warm day`.
5. Line 16 checks `is_raining`. It is already a `bool`, so no comparison is needed. It is `False`, so the `else` on line 18 runs and line 19 prints `No umbrella needed`.

**Notice:** the `elif` conditions go from the highest temperature to the lowest. If line 9 (`>= 15`) came first, every warm day would be called "Mild day".

**Try it yourself:** change `temperature` to `10` and `is_raining` to `True`. Predict both lines of output before you press Run.
