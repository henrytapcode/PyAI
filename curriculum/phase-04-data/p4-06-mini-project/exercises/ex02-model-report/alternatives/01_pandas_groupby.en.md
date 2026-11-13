# Pure pandas `groupby().agg()` instead of SQLite (comparison only)

Note: Exercise 2's prompt asks you to aggregate with SQLite, so keep SQL in your main solution—this alternative intentionally skips SQL just to compare the two styles. Instead of copying the `DataFrame` into SQLite, it creates a float helper column `is_error` and uses pandas named aggregation `agg(new_col=("col", "func"))`, which lets you name each output column (`requests=("request_id", "count")`, `total_tokens=("tokens", "sum")`) in one `.agg(...)` call before rounding and sorting.

Use **SQL** when the logs already live in a database (so you filter and aggregate before loading into Python) or when teammates share SQL reports; use **pandas** when the table is already in RAM after cleaning and you want to avoid serialising data into a temporary database.
