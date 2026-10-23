# Checking a config early

**What it shows:** `raise` for your own clear errors, plus `except ... as err`, `else` and `finally` working together.

**Step by step**
1. Lines 3–4 stop early if the required `model` key is missing, with a message that says exactly what to fix.
2. Line 5 reads `temperature` with `.get()` and a default of `0.7`, so a missing temperature is fine.
3. Lines 6–7 reject a temperature outside 0 to 2. The f-string puts the bad value in the message, which makes debugging much faster.
4. Lines 17–25 try each config. If `check_config` raises, `except ValueError as err` prints the message.
5. The `else` block (line 22) runs only when nothing was raised. The `finally` block (line 24) runs every time, so you see `-- checked one config` three times.

**Notice:** the validation function does not print or decide what to do. It only raises. The caller decides whether to show a message, use a default, or stop.

**Try it yourself:** change the second config to `{"model": "small", "temperature": -1}`. Which message appears? (`temperature must be between 0 and 2, got -1`.)
