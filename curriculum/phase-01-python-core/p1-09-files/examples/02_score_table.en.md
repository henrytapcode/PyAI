# Score table in CSV

**What it shows:** the full CSV round trip: write rows with `DictWriter`, read them back with `DictReader`, convert text to numbers and compute averages.

**Step by step**
1. Lines 6–11 describe the data as a list of dicts. Each dict is one row.
2. Lines 16–19 write the file. `writeheader()` writes the line `name,score`, and `writerows(rows)` writes every dict as one line.
3. Lines 23–32 read it back. `csv.DictReader(f)` gives one dict per row, using the header as keys.
4. Line 26 uses `float(row["score"])` because CSV values always come back as text.
5. Lines 34–35 print the average per student with two decimals.

**Notice:** both `open` calls pass `newline=""`. The `csv` module needs it, otherwise you can get blank lines on Windows.

**Try it yourself:** add `{"name": "An", "score": 10}` to `rows` and run again. A new line `An: 10.00` should appear at the end.
