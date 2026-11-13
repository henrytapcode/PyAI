Write two functions to build and plot the per-model API usage report from an already-cleaned `DataFrame`. Write your code inside `model_report` and `plot_report` and `return` each result.

**Example**

Input `df` (already cleaned):

```text
  request_id   model  tokens  latency_ms status  rating
0        r01  gpt-4o    1200       850.0     ok     5.0
1        r02  gpt-4o     800         NaN  error     NaN
2        r03    mini     300       200.0     ok     4.0
```

`model_report(df)` returns:

```text
    model  requests  total_tokens  error_rate  avg_latency  avg_rating
0  gpt-4o         2          2000         0.5        850.0         5.0
1    mini         1           300         0.0        200.0         4.0
```

And `plot_report(report)` draws a bar chart with `"gpt-4o"` (`2000`) then `"mini"` (`300`), returning `(fig, ax)`.

**Rules**

- `model_report(df)`:
  - Load `df` into an in-memory SQLite database (`sqlite3.connect(":memory:")`) using `df.to_sql(...)`, run **one** `GROUP BY model` query via `pd.read_sql_query(...)`, and close the connection before returning.
  - Return columns in exact order: `["model", "requests", "total_tokens", "error_rate", "avg_latency", "avg_rating"]`.
  - Round `error_rate` to `3` decimal places, `avg_latency` to `1` decimal place, and `avg_rating` to `2` decimal places (if a model has no valid ratings, `avg_rating` is `NaN`).
  - Sort by `total_tokens` descending, breaking ties by `model` ascending, with index `0..n-1`.
  - Do not modify `df`.
- `plot_report(report)`:
  - Draw a bar chart of `total_tokens` by `model` in the exact order of `report`.
  - Set title `"Tokens by model"` and y-axis label `"tokens"`.
  - Return `(fig, ax)` without calling `plt.show()`, and do not modify `report`.
