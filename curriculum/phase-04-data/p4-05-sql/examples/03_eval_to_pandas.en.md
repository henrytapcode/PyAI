# Loading SQLite eval results into pandas

**What it shows:** filtering rows in SQL with `pd.read_sql_query(sql, conn, params=...)` and then computing per-model mean scores in pandas.

**Step by step**
1. Lines 5–13 create the `eval_runs` table (`model`, `task`, `score`).
2. Lines 15–27 insert six evaluation runs across three models and two tasks.
3. Lines 29–35 run `pd.read_sql_query` with `params=(0.75,)` so SQL drops the `0.74` run before pandas receives the data.
4. Lines 36–44 group the resulting DataFrame by `"model"`, average `"score"`, reset the index to keep `"model"` as a column, round to 2 decimal places, sort descending, and print the small summary table.

**Notice:** filtering with `WHERE score >= ?` in SQL keeps unwanted rows out of the DataFrame from the start, which saves memory on large tables.

**Try it yourself:** lower `params=(0.75,)` to `params=(0.70,)` and see how `mini`'s mean score changes when `0.74` is included.
