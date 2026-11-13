# API costs from CSV

**What it shows:** reading CSV text with `io.StringIO`, adding computed columns, and finding the three most expensive requests.

**Step by step**
1. Lines 5–10 store five API call records as a multi-line CSV string.
2. Line 12 parses the CSV string into a DataFrame with `pd.read_csv(io.StringIO(csv_data))`.
3. Lines 13–14 compute `total_tokens` from two existing columns and `cost` rounded to 4 decimal places.
4. Line 16 sorts by `cost` descending, resets the index, and takes the first 3 rows with `.head(3)`.
5. Lines 18–19 print the top 3 rows (selecting 3 columns) and the total cost across all calls.

**Notice:** wrapping `df["cost"].sum()` in `float(...)` before `round(...)` prints a clean Python float instead of a NumPy scalar type.

**Try it yourself:** change the rate `0.002` on line 14 to `0.005` and see how the top-3 costs and total cost scale.
