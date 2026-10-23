# Parse log lines

**What it shows:** `startswith()` to filter lines, `split(",")` to break a line into fields, and `join()` to build a summary.

**Step by step**
1. Lines 2–6 hold four log lines. Each is one string with three fields separated by commas.
2. Line 9 creates an empty list `errors` to collect results.
3. Lines 10–11 loop over the lines and keep only those that start with `"ERROR"`.
4. Line 12 splits a line like `"ERROR,gpt-large,timeout"` into the list `["ERROR", "gpt-large", "timeout"]`. Lines 13–15 pick the fields out by index.
5. Line 16 builds a short message with an f-string and appends it. Lines 18–19 print the count and join all messages with `" | "`.

**Notice:** `split` and `join` are used in opposite directions here: one to take a line apart, one to put the report together.

**Try it yourself:** also collect the `INFO` lines into a second list and print how many there are.
