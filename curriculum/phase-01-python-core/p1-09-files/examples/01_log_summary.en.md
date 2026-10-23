# Log summary

**What it shows:** writing a file with `"w"`, adding to it with `"a"`, then reading it line by line to count things.

**Step by step**
1. Lines 2–3 import `tempfile` and `Path`. Line 5 creates a temporary folder, and line 6 builds the path `app.log` inside it with `/`.
2. Lines 8–10 open the file with `"w"` and write two lines. Each one ends with `\n`.
3. Lines 11–13 open it again with `"a"` and add two more lines. Nothing is erased.
4. Lines 16–22 loop over the file. `line.strip().split(" ")[0]` removes the newline, cuts the line into words and keeps the first word, the log level.
5. Lines 24–25 print the file name and suffix, then the counts dictionary.

**Notice:** the `if level in counts` check is needed because a key must exist before you can do `+= 1` on it.

**Try it yourself:** change the second `with` block from `"a"` to `"w"` and run again. Only the last two lines survive, so the output becomes `{'INFO': 2}`.
