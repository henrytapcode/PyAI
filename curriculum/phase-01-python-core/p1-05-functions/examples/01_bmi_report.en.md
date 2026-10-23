# BMI report: functions calling functions

**What it shows:** three small functions, each doing one job, combined into a report. This is how real programs are built.

**Step by step**
1. Lines 2–4 define `bmi`. It takes two parameters and **returns** one number. Nothing is printed here.
2. Lines 7–13 define `bmi_category`. Each `return` ends the function, so the next `if` only runs when the previous one did not match. That is why `value < 25` really means "from 18.5 up to 25".
3. Lines 16–19 define `report`. Line 17 calls `bmi(...)` and stores what comes back in `value`. Line 18 hands `value` to `bmi_category`. Line 19 builds the final text. In the f-string, `:.1f` means "show 1 decimal place".
4. Lines 22–24 call `report` three times with different arguments. Nothing before line 22 prints anything: the `def` lines only *define*.

**Notice:** `report` never repeats the BMI formula. If the formula changes, you edit `bmi` in one place.

**Try it yourself:** press **Visualize** and watch a new frame appear for `report`, then another for `bmi` inside it, and disappear again when each `return` runs. Then add `print(report("You", 60, 1.70))`.
