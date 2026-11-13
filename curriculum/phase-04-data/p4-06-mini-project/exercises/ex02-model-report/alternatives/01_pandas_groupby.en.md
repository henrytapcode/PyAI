# Pure pandas `groupby().agg()` instead of SQLite

Instead of copying the `DataFrame` into SQLite and running SQL, this approach computes a boolean-to-float `is_error` helper column on a copy and aggregates every metric directly with `groupby("model", as_index=False).agg(...)`, then rounds and sorts.

Use **SQL** when the logs already live in a database (so you filter and aggregate before loading into Python) or when teammates share SQL reports; use **pandas** when the table is already in RAM after cleaning and you want to avoid serialising data into a temporary database.
