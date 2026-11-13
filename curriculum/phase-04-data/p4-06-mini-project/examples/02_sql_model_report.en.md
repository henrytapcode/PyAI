# Building the SQL model report

**What it shows:** how to clean raw log rows with pandas, load the clean table into an in-memory SQLite database, and compute all per-model metrics in one `GROUP BY` query.

**Step by step**
1. Lines 22–30 normalise `model`, parse `tokens` (dropping commas), coerce `latency_ms` and `rating`, clear out-of-range ratings, deduplicate `request_id`, drop rows missing `tokens`, and cast `tokens` to `"int64"`.
2. Lines 32–46 write the clean table to SQLite with `df.to_sql("requests", conn, index=False)`, run one `GROUP BY model` query via `pd.read_sql_query(...)`, and close the connection.
3. Lines 48–52 print each model's summary on one compact f-string line.

**Notice:** `AVG(status = 'error')` works in SQLite because `status = 'error'` evaluates to `1` for errors and `0` for `ok`, so the average is directly the error rate.

**Try it yourself:** change `ORDER BY total_tokens DESC, model ASC` to `ORDER BY error_rate DESC, model ASC` to rank models from most error-prone to most reliable.
