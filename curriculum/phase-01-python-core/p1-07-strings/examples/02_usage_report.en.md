# Usage report

**What it shows:** format specs in f-strings (`:<12`, `:>12,`, `:>14.4f`) building a table with neat columns.

**Step by step**
1. Lines 2–5 store usage per model in a dictionary of dictionaries: each model name maps to its token count and its price per million tokens.
2. Line 8 prints the header. The column names are strings, so `'model':<12` left-aligns in 12 characters and `'tokens':>12` right-aligns in 12.
3. Lines 10–14 loop over the models. `cost` is `tokens / 1000000 * price`, and `total` collects the sum, like the accumulator pattern from the loops lesson.
4. Line 14 prints each row with the **same widths as the header** (12, 12, 14), which is why the columns line up. `:>12,` adds thousands separators and `:>14.4f` shows 4 decimals.
5. Lines 16–17 draw a line of 38 dashes (12 + 12 + 14) and print the total.

**Notice:** the format spec changes only how a value is *shown*. `tokens` is still the plain number `1250000` inside the program.

**Try it yourself:** change `:>14.4f` to `:>14.2f` on both lines and check that the columns still line up.
