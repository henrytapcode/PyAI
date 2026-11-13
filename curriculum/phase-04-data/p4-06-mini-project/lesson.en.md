Your team runs a chatbot across three models and wants weekly answers: which model burns the most tokens, which one is slowest, which one fails most often, and how users rate each one. All you have is a raw CSV export of request logs—turning noisy logs like this into a clear summary is something AI engineers do every week.

This project combines everything from phase 4—cleaning with pandas, aggregating with SQLite, and plotting a chart—and introduces six handy tools along the way:

**New in this lesson**
- `.astype(str)` — converts a column to strings before calling `.str` so numeric-only columns do not crash.
- `Series.where(cond)` — keeps values where the condition is `True` and turns all other positions into `NaN`.
- `df.to_sql(name, conn, index=False, if_exists=...)` — writes a `DataFrame` straight into a SQLite table (`if_exists="replace"` overwrites an existing table).
- `AVG(status = 'error')` — SQLite evaluates `status = 'error'` as `1` or `0`, so its average gives the error rate directly.
- `df.iterrows()` — loops over a small `DataFrame`, yielding `(index, row)` pairs.
- `f"{name:<7}"` — pads a string with spaces to width `7` (left-aligned) so printed rows line up.

## 1. The plan

Start with the pipeline from raw text to final chart before writing any function:

```mermaid
flowchart LR
    A["Raw CSV"] --> B["Clean (pandas)"]
    B --> C["Clean table"]
    C --> D["SQLite"]
    D --> E["Model report (SQL)"]
    E --> F["Bar chart"]
```

Break the work into three small pieces, each with one job:

| Piece | Input | Output |
|---|---|---|
| `load_and_clean(csv_text)` | raw CSV string | clean 6-column `DataFrame` |
| `model_report(df)` | clean `DataFrame` | sorted per-model summary `DataFrame` |
| `plot_report(report)` | summary `DataFrame` | `(fig, ax)` bar chart |

Exercise 1 builds `load_and_clean`. Exercise 2 builds `model_report` and `plot_report`.

## 2. Inspecting the raw logs

Never clean blind—load the CSV with `pd.read_csv(io.StringIO(csv_text))` and inspect its shape, column types, missing counts, and messy categories first:

```python
import io
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5
r07,claude,650,580,ok,4
r08, CLAUDE,700,640,error,2
r09,claude ,500,timeout,ok,
r07,claude,999,700,ok,3
r10,mini,300,210,ok,4
r11, MINI ,250,190,ok,3
r12,mini,350,230,ok,5"""

df = pd.read_csv(io.StringIO(csv_text))
print(df[["request_id", "model", "tokens", "rating"]].head(5))
#   request_id    model tokens  rating
# 0        r01   GPT-4o  1,200     5.0
# 1        r02   gpt_4o    900     4.0
# 2        r02   gpt_4o    950     1.0
# 3        r03  GPT-4o   1,100     NaN
# 4        r04   gpt_4o    800     9.0

print(df.shape)
# (14, 6)
print(df.dtypes)
# request_id     object
# model          object
# tokens         object
# latency_ms     object
# status         object
# rating        float64
# dtype: object

print(df.isna().sum())
# request_id    0
# model         0
# tokens        1
# latency_ms    1
# status        0
# rating        2
# dtype: int64

print(df["model"].value_counts().head(4))
# model
# gpt_4o     4
# mini       2
# claude     2
#  GPT-4o    1
# Name: count, dtype: int64
```

Every problem jumps out in those first few rows:

```text
request_id, model,     tokens,  latency_ms, status, rating
r02,        gpt_4o,    900,     920,        ok,     4
r02,        gpt_4o,    950,     999,        error,  1      <- duplicate request_id
r03,        GPT-4o ,   "1,100", N/A,        error,         <- spaces, comma, N/A, blank
r04,        gpt_4o,    800,     790,        error,  9      <- underscore, rating 9 > 5
r05,        gpt_4o,    ,        600,        ok,     4      <- missing tokens
r09,        claude ,   500,     timeout,    ok,            <- text in latency_ms
```

Notice that `latency_ms` shows only `1` missing cell (`N/A`) at first because `"timeout"` stays as text (`object`) until we coerce the column to numbers.

## 3. Part 1: cleaning the logs

We fix the raw table step by step in a deliberate order. First, normalise `model` names by stripping spaces, lowercasing, and replacing `"_"` with `"-"`:

```python
import io
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5
r07,claude,650,580,ok,4
r08, CLAUDE,700,640,error,2
r09,claude ,500,timeout,ok,
r07,claude,999,700,ok,3
r10,mini,300,210,ok,4
r11, MINI ,250,190,ok,3
r12,mini,350,230,ok,5"""

df = pd.read_csv(io.StringIO(csv_text))
df["model"] = df["model"].str.strip().str.lower().str.replace("_", "-", regex=False)
print(df["model"].value_counts())
# model
# gpt-4o    6
# claude    5
# mini      3
# Name: count, dtype: int64
```

Next, strip commas from `tokens` and coerce both `tokens` and `latency_ms` to numbers with `pd.to_numeric(..., errors="coerce")`. Calling `.astype(str)` before `.str.replace` is essential: if a batch has no text at all (only plain numbers), pandas reads it as numeric and `.str` raises `AttributeError: Can only use .str accessor with string values!`—`.astype(str)` keeps `.str` safe:

```python
import io
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4"""

df = pd.read_csv(io.StringIO(csv_text))
clean_tokens = df["tokens"].astype(str).str.replace(",", "", regex=False)
df["tokens"] = pd.to_numeric(clean_tokens, errors="coerce")
df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
print(df[["request_id", "tokens", "latency_ms"]].iloc[2:6])
#   request_id  tokens  latency_ms
# 2        r02   950.0       999.0
# 3        r03  1100.0         NaN
# 4        r04   800.0       790.0
# 5        r05     NaN       600.0
print(df[["tokens", "latency_ms"]].dtypes)
# tokens        float64
# latency_ms    float64
# dtype: object
```

Notice `tokens` becomes `float64` temporarily because row `r05` is `NaN`; we cast `tokens` to `"int64"` only after dropping missing `tokens` rows. For `rating`, coerce to numbers first and turn values outside `1..5` into `NaN` with `.where(df["rating"].between(1, 5))` (which keeps values where the condition is `True` and turns other positions into `NaN`):

```python
import io
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5"""

df = pd.read_csv(io.StringIO(csv_text))
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].where(df["rating"].between(1, 5))
print(df[["request_id", "rating"]].iloc[3:7])
#   request_id  rating
# 3        r03     NaN
# 4        r04     NaN
# 5        r05     4.0
# 6        r06     5.0
```

Finally, mask out-of-range ratings, drop duplicate `request_id` rows (`keep="first"`), drop rows missing `tokens`, reset the index, and cast `tokens` to `"int64"`. Notice two differences from p4-03: we drop rows only when the broken field is the row's main value (like `rating` in p4-03's ratings table), whereas here we mask `rating` to `NaN` so `tokens`, `latency_ms`, and `status` remain usable; and we use `keep="first"` because the first logged request is the original (whereas in p4-03 a newer rating replaced an older one). Press **Visualize** on this block and watch `df` shrink step by step:

```python
import io
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4"""

df = pd.read_csv(io.StringIO(csv_text))
df["rating"] = df["rating"].where(df["rating"].between(1, 5))
df = df.drop_duplicates(subset=["request_id"], keep="first")
df = df.dropna(subset=["tokens"]).reset_index(drop=True)
df["tokens"] = df["tokens"].astype("int64")
print(df[["request_id", "tokens", "rating"]])
#   request_id  tokens  rating
# 0        r02     900     4.0
# 1        r04     800     NaN
```

Here is the full cleaning checklist at a glance:

| problem | fix |
|---|---|
| Spaces, mixed case, `_` in `model` | `.str.strip().str.lower().str.replace("_", "-", regex=False)` |
| Commas and blanks in `tokens` | strip `","`, `pd.to_numeric(..., errors="coerce")`, `dropna`, `.astype("int64")` |
| `"N/A"` or `"timeout"` in `latency_ms` | `pd.to_numeric(..., errors="coerce")` |
| Out-of-range `rating` (`9`) | `df["rating"].where(df["rating"].between(1, 5))` |
| Duplicate `request_id` rows | `df.drop_duplicates(subset=["request_id"], keep="first")` |
| Gapped row index after drops | `.reset_index(drop=True)` |

## 4. Part 2: reporting with SQL

With the table clean, write it to an in-memory SQLite database via `df.to_sql("requests", conn, index=False)` and compute every metric in a single `GROUP BY model` query. Two SQLite tricks make the query short:

- `status = 'error'` evaluates to `1` for errors and `0` for `"ok"`, so `AVG(status = 'error')` gives the error rate directly.
- `AVG(latency_ms)` and `AVG(rating)` ignore `NULL` values automatically, so missing timings or ratings never pull the average down.

```python
import io
import sqlite3
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5
r07,claude,650,580,ok,4
r08, CLAUDE,700,640,error,2
r09,claude ,500,timeout,ok,
r07,claude,999,700,ok,3
r10,mini,300,210,ok,4
r11, MINI ,250,190,ok,3
r12,mini,350,230,ok,5"""

df = pd.read_csv(io.StringIO(csv_text))
df["model"] = df["model"].str.strip().str.lower().str.replace("_", "-", regex=False)
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].where(df["rating"].between(1, 5))
df = df.drop_duplicates(subset=["request_id"], keep="first")
df = df.dropna(subset=["tokens"]).reset_index(drop=True)
df["tokens"] = df["tokens"].astype("int64")

conn = sqlite3.connect(":memory:")
df.to_sql("requests", conn, index=False)
report = pd.read_sql_query("""
    SELECT
        model,
        COUNT(*) AS requests,
        SUM(tokens) AS total_tokens,
        ROUND(AVG(status = 'error'), 3) AS error_rate,
        ROUND(AVG(latency_ms), 1) AS avg_latency,
        ROUND(AVG(rating), 2) AS avg_rating
    FROM requests
    GROUP BY model
    ORDER BY total_tokens DESC, model ASC
""", conn)
conn.close()

for _, row in report.iterrows():
    print(
        f"{row['model']:<7} req={row['requests']} tok={row['total_tokens']} "
        f"err={row['error_rate']} lat={row['avg_latency']} rat={row['avg_rating']}"
    )
# gpt-4o  req=4 tok=4000 err=0.5 lat=853.3 rat=4.5
# claude  req=4 tok=2600 err=0.25 lat=613.3 rat=3.67
# mini    req=3 tok=900 err=0.0 lat=210.0 rat=4.0
```

Trace how SQLite aggregates the 4 cleaned rows of `gpt-4o`:

| request_id | tokens | status (`error`=1) | latency_ms | rating |
|---|---|---|---|---|
| `r01` | `1200` | `ok` (`0`) | `850.0` | `5.0` |
| `r02` | `900` | `ok` (`0`) | `920.0` | `4.0` |
| `r03` | `1100` | `error` (`1`) | `NaN` | `NaN` |
| `r04` | `800` | `error` (`1`) | `790.0` | `NaN` |
| **summary** | **4000** | **0.5** (`2 / 4`) | **853.3** (`2560 / 3`) | **4.5** (`9 / 2`) |

Notice `ORDER BY total_tokens DESC, model ASC` sorts the biggest token consumer first and breaks any tie alphabetically by model name.

## 5. Part 3: plotting and reading the report

Feed the sorted `report` columns straight into `ax.bar(...)` with clear titles and axis labels:

```python
import matplotlib.pyplot as plt
import pandas as pd

report = pd.DataFrame({
    "model": ["gpt-4o", "claude", "mini"],
    "total_tokens": [4000, 2600, 900],
})

fig, ax = plt.subplots()
ax.bar(report["model"].tolist(), report["total_tokens"].tolist())
ax.set_title("Tokens by model")
ax.set_xlabel("model")
ax.set_ylabel("tokens")
plt.show()
# (shows bar chart: gpt-4o 4000, claude 2600, mini 900)
```

Reading the report: `gpt-4o` should be optimised first because it uses the most tokens (`4000`, over half the total), has the highest latency (`853.3 ms`), and fails half the time (`error_rate = 0.5`). Meanwhile, `mini` handles requests in `210.0 ms` with `0.0` errors and a solid `4.0` rating, so routing simpler prompts to `mini` or adding retries and caching for `gpt-4o` gives the biggest immediate gain.

> [!TIP]
> A good report answers a specific question. Numbers and charts are only half the job—always finish with one or two concrete sentences saying what the team should do next.

## 6. Common mistakes

**Calling `to_sql` twice with the same table name.** By default `to_sql` fails if the table already exists:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
df = pd.DataFrame({"model": ["mini"], "tokens": [100]})
df.to_sql("requests", conn, index=False)
# Wrong: df.to_sql("requests", conn, index=False)
# ValueError: Table 'requests' already exists.

df.to_sql("requests", conn, index=False, if_exists="replace")
print(conn.execute("SELECT COUNT(*) FROM requests").fetchone())
# (1,)
conn.close()
```

Fix: pass `if_exists="replace"` when re-running against an existing connection.

**Grouping before normalising `model` names.** Skipping `.strip().lower()` and `"_"` replacement splits one model across multiple rows in SQL:

```python
import sqlite3
import pandas as pd

raw = pd.DataFrame({
    "model": [" GPT-4o", "gpt_4o", "Claude "],
    "tokens": [1200, 900, 750],
})
conn = sqlite3.connect(":memory:")
raw.to_sql("requests", conn, index=False)
bad = pd.read_sql_query(
    "SELECT model, SUM(tokens) AS total FROM requests GROUP BY model ORDER BY model",
    conn,
)
print(bad)
#      model  total
# 0   GPT-4o   1200
# 1  Claude     750
# 2   gpt_4o    900
conn.close()
```

Fix: always run the full cleaning pipeline before loading into SQLite.

**Casting `tokens` to `"int64"` before dropping missing rows.** Integer columns cannot hold `NaN`, so casting too early crashes:

```python
import pandas as pd

tokens = pd.Series([1200.0, float("nan"), 800.0])
# Wrong: tokens.astype("int64")
# pandas.errors.IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer

clean_tokens = tokens.dropna().astype("int64")
print(clean_tokens.tolist())
# [1200, 800]
```

Fix: call `.dropna(...)` first, then `.astype("int64")`.

## Recap

- Plan the pipeline (`load_and_clean` → `model_report` → `plot_report`) so each function has one clear input and output.
- Inspect raw CSV data with `shape`, `dtypes`, `isna().sum()`, and `value_counts()` before touching any column.
- Clean in the order used in §3: normalise text, coerce numbers, mask out-of-range ratings to `NaN`, deduplicate (`keep="first"`), drop missing `tokens`, reset index, then cast `"int64"`.
- Write clean tables to SQLite (`to_sql`), compute `COUNT`, `SUM`, `AVG(status = 'error')`, and `ROUND(AVG(...))` in one `GROUP BY` query with `ORDER BY` + tie-breaker, and load with `pd.read_sql_query`.
- Plot sorted bars with clear labels and end with an actionable takeaway answering the team's question.

## Take it further

Once both exercises pass, try extending the report on your own:

- Add a `cost_usd` column using a price-per-1k-tokens dictionary for each model and rank models by total spend.
- Plot a second chart comparing `avg_latency` or `error_rate` across models.
- Export the final `report` DataFrame to a CSV file with `report.to_csv(..., index=False)`.
