# Converting messy price strings to numbers

**What it shows:** stripping thousands commas from text prices, coercing unreadable values to `NaN` with `pd.to_numeric(..., errors="coerce")`, and casting valid rows to `int64`.

**Step by step**
1. Lines 4–7 build `orders` with mixed price strings (`"1,200"`, `"N/A"`, `" 350 "`, `"free"`, `"890"`).
2. Lines 9–10 remove commas with `.str.replace(",", "", regex=False)` and coerce the column to numbers.
3. Lines 12–13 count how many entries became `NaN` (`2`) and print the count as a plain Python `int`.
4. Lines 15–18 drop the `NaN` rows, cast `price` to `"int64"`, and print the clean table and total revenue.

**Notice:** without `errors="coerce"`, `pd.to_numeric` would crash with a `ValueError` as soon as it hits `"N/A"` or `"free"`.

**Try it yourself:** replace `"free"` on line 6 with `" 450 "` and watch `Unreadable prices` drop from `2` to `1`.
