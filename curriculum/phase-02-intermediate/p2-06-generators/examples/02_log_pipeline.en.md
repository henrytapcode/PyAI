# Log pipeline

**What it shows:** two small generators chained together to find the `ERROR` lines in a file. The file is read one line at a time.

**Step by step**
1. Lines 6–9 define `read_lines`. It opens the file and yields each line with the spaces and the newline removed.
2. Lines 12–15 define `only_errors`. It takes any iterable of lines and yields only those that contain `ERROR`.
3. Lines 18–25 create a temporary folder and write a five-line log file inside it.
4. Line 27 chains the two stages. Still nothing has been read. Line 28 asks for the first error, so only the first two lines of the file are processed.
5. Line 29 collects the rest into a list. Line 31 builds a **new** pipeline to count the errors with `sum`.

**Notice:** line 31 starts a fresh pipeline instead of reusing `errors`, because `errors` was already used up by lines 28–29.

**Try it yourself:** add `f.write("ERROR gpu memory\n")` after line 25. The final count should become 3.
