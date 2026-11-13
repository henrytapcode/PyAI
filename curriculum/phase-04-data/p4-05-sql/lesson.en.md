Real AI applications store chat histories, user feedback, and evaluation scores in a **database** rather than loose lists in memory. **SQL** (Structured Query Language) is the shared language for asking a database questions, and **SQLite** comes built into Python's standard library (`import sqlite3`) so you can run a full SQL database without installing a server.

## 1. Connecting and creating a table

A SQL database organises data into named **tables**, where every **column** has a name and a type and every **row** holds one record. Think of a table like a spreadsheet sheet whose column types are declared upfront (`INTEGER` for whole numbers, `TEXT` for strings, `REAL` for floats), plus an optional `PRIMARY KEY` column that uniquely identifies each row.

```text
table: messages
+----+------+-------------+----------------------+
| id | user | role        | text                 |
|INT | TEXT | TEXT        | TEXT                 |
+----+------+-------------+----------------------+
|  1 | "an" | "user"      | "Summarise this PDF" |
|  2 | "an" | "assistant" | "Here is a summary." |
+----+------+-------------+----------------------+
```

Calling `sqlite3.connect(":memory:")` opens a temporary database in RAM, and `conn.execute(...)` runs a SQL statement such as `CREATE TABLE`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        user TEXT,
        role TEXT,
        text TEXT
    )
""")
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
).fetchall()
print(tables)
# [('messages',)]
conn.close()
```

Notice two conventions we will keep throughout this lesson: SQL keywords like `CREATE TABLE`, `INTEGER`, and `PRIMARY KEY` are written in UPPERCASE, while table and column names stay lowercase.

## 2. Inserting rows

Use `INSERT INTO table (col1, col2, ...) VALUES (?, ?, ...)` to add rows, putting a `?` **placeholder** wherever a Python value goes and passing the values separately as a tuple. For several rows at once, pass a list of tuples to `conn.executemany(...)` instead of looping by hand.

Wrapping inserts in `with conn:` — the **context manager** pattern from Phase 2 — automatically calls `conn.commit()` when the block finishes without errors (or rolls back if an exception occurs). Remember that an in-memory `:memory:` database disappears when your program ends; real projects pass a file path such as `sqlite3.connect("app.db")` so rows stay on disk.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        user TEXT,
        role TEXT,
        text TEXT
    )
""")

rows = [
    ("an", "user", "Summarise this PDF"),
    ("an", "assistant", "Here is a summary."),
    ("binh", "user", "Translate to Vietnamese"),
]
with conn:
    conn.execute(
        "INSERT INTO messages (user, role, text) VALUES (?, ?, ?)",
        ("an", "user", "Hello!"),
    )
    conn.executemany(
        "INSERT INTO messages (user, role, text) VALUES (?, ?, ?)",
        rows,
    )

count = conn.execute("SELECT COUNT(*) FROM messages").fetchone()
print(count)
# (4,)
conn.close()
```

Notice that `id` was left out of the column list because SQLite automatically fills an `INTEGER PRIMARY KEY` column with `1, 2, 3, 4`.

## 3. Querying with SELECT

A `SELECT` **query** reads columns from a table: `.fetchall()` returns every matching row as a list of Python tuples, while `.fetchone()` returns only the first tuple (or `None` if nothing matched). You filter rows with `WHERE` (`=`, `>`, `AND`, `OR`, `LIKE` with `%` as a wildcard), sort them with `ORDER BY ... DESC` (or `ASC`), and cap the count with `LIMIT`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE prompts (
        id INTEGER PRIMARY KEY,
        user TEXT,
        model TEXT,
        tokens INTEGER
    )
""")
with conn:
    conn.executemany(
        "INSERT INTO prompts (user, model, tokens) VALUES (?, ?, ?)",
        [
            ("an", "gpt-4o", 320),
            ("binh", "mini", 110),
            ("an", "gpt-4o-mini", 480),
            ("chi", "claude", 260),
        ],
    )

long_an = conn.execute("""
    SELECT id, model, tokens
    FROM prompts
    WHERE user = ? AND (tokens > ? OR model LIKE ?)
    ORDER BY tokens DESC
    LIMIT 2
""", ("an", 300, "gpt%")).fetchall()
print(long_an)
# [(3, 'gpt-4o-mini', 480), (1, 'gpt-4o', 320)]

top_one = conn.execute(
    "SELECT user, tokens FROM prompts ORDER BY tokens DESC LIMIT 1"
).fetchone()
print(top_one)
# ('an', 480)
conn.close()
```

Parentheses around `(tokens > ? OR model LIKE ?)` ensure `AND` binds to the whole `OR` pair rather than just the first condition. Now look at a smaller query that loops over the returned tuples:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE scores (id INTEGER PRIMARY KEY, model TEXT, score REAL)")
with conn:
    conn.executemany(
        "INSERT INTO scores (model, score) VALUES (?, ?)",
        [("mini", 0.78), ("gpt-4o", 0.91), ("claude", 0.88)],
    )

rows = conn.execute(
    "SELECT model, score FROM scores WHERE score > 0.80 ORDER BY score DESC"
).fetchall()
for model, score in rows:
    print(f"{model}: {score}")
# gpt-4o: 0.91
# claude: 0.88
conn.close()
```

Press **Visualize** on this block and watch `rows` fill with the sorted query result before `model` and `score` unpack one row per iteration.

## 4. Aggregating with GROUP BY

Just like `.groupby()` in pandas, `GROUP BY col` collapses rows sharing the same value into one summary row so you can compute `COUNT(*)`, `SUM(...)`, and `AVG(...)` (plus `ROUND(x, 2)` for clean decimals). To keep only groups that meet a summary condition — such as models with at least 2 ratings — add `HAVING` after `GROUP BY`.

Here is how `GROUP BY model` collapses five feedback rows before `HAVING COUNT(*) >= 2` drops `claude`:

| model | rows | ratings | AVG |
|---|---|---|---|
| `claude` | 1 | `5` | `5.0` |
| `gpt-4o` | 2 | `5, 4` | `4.5` |
| `mini` | 2 | `3, 4` | `3.5` |

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE feedback (id INTEGER PRIMARY KEY, model TEXT, rating INTEGER)")
with conn:
    conn.executemany(
        "INSERT INTO feedback (model, rating) VALUES (?, ?)",
        [
            ("gpt-4o", 5),
            ("mini", 3),
            ("gpt-4o", 4),
            ("mini", 4),
            ("claude", 5),
        ],
    )

stats = conn.execute("""
    SELECT
        model,
        COUNT(*) AS total,
        SUM(rating) AS pts,
        ROUND(AVG(rating), 2) AS avg_rating
    FROM feedback
    GROUP BY model
    HAVING COUNT(*) >= 2
    ORDER BY avg_rating DESC, model ASC
""").fetchall()
print(stats)
# [('gpt-4o', 2, 9, 4.5), ('mini', 2, 7, 3.5)]
conn.close()
```

Notice `ORDER BY avg_rating DESC, model ASC`: adding a second tie-breaker column guarantees a predictable order even when two models share the same average.

## 5. SQL and pandas

When you are ready to analyse or plot query results, `pd.read_sql_query(sql, conn, params=(...))` executes your SQL query and returns a pandas `DataFrame` directly. Filtering and grouping in SQL before calling `pd.read_sql_query` avoids loading millions of unused rows into Python memory.

| SQL | pandas |
|---|---|
| `WHERE rating >= 4` | `df[df["rating"] >= 4]` |
| `ORDER BY score DESC` | `df.sort_values("score", ascending=False)` |
| `GROUP BY model` | `df.groupby("model")` |
| `LIMIT 5` | `df.head(5)` |

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE runs (model TEXT, task TEXT, score REAL)")
with conn:
    conn.executemany(
        "INSERT INTO runs (model, task, score) VALUES (?, ?, ?)",
        [
            ("gpt-4o", "qa", 0.92),
            ("mini", "qa", 0.79),
            ("gpt-4o", "summary", 0.88),
            ("mini", "summary", 0.74),
        ],
    )

sql = """
    SELECT model, task, score
    FROM runs
    WHERE score >= ?
    ORDER BY score DESC
"""
df = pd.read_sql_query(sql, conn, params=(0.80,))
print(df)
#     model     task  score
# 0  gpt-4o       qa   0.92
# 1  gpt-4o  summary   0.88
conn.close()
```

Notice that `params=(0.80,)` passes the threshold safely as a tuple instead of embedding numbers or strings directly into the SQL text.

## 6. The order SQL actually runs

You write `SELECT` at the top of a query, yet SQL executes the clauses in a different order behind the scenes:

```mermaid
flowchart LR
    A["1. FROM"] --> B["2. WHERE"]
    B --> C["3. GROUP BY"]
    C --> D["4. HAVING"]
    D --> E["5. SELECT"]
    E --> F["6. ORDER BY"]
    F --> G["7. LIMIT"]
```

This execution order explains why `WHERE` cannot reference `COUNT(*)` or `AVG(rating)` while `HAVING` can: `WHERE` filters individual rows in step 2 *before* `GROUP BY` forms any groups, whereas `HAVING` filters whole groups in step 4 *after* aggregates exist.

## 7. Common mistakes

**Building SQL with f-strings instead of `?` placeholders.** Concatenating user text into a SQL string crashes on apostrophes like `"O'Brien"` and opens the door to **SQL injection**, where crafted input alters the query itself.

> [!WARNING]
> Never build SQL queries with f-strings or `+` from user input. Attackers can inject extra SQL syntax to read or delete data you never meant to expose; always use `?` **parameterized queries**.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT)")
name = "O'Brien"
# Wrong: conn.execute(f"INSERT INTO users (name) VALUES ('{name}')")
# sqlite3.OperationalError: near "Brien": syntax error

with conn:
    conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
print(conn.execute("SELECT name FROM users ORDER BY name").fetchall())
# [("O'Brien",)]
conn.close()
```

Fix: leave `?` inside the SQL string and pass `(name,)` as the second argument to `execute`.

**Forgetting the trailing comma in a one-item parameter tuple.** Writing `("ab")` creates a two-character string instead of a tuple, so SQLite tries to bind two characters to one `?`:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT)")
with conn:
    conn.execute("INSERT INTO users (name) VALUES (?)", ("ab",))

# Wrong: conn.execute("SELECT name FROM users WHERE name = ?", ("ab"))
# sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 2 supplied.
rows = conn.execute("SELECT name FROM users WHERE name = ?", ("ab",)).fetchall()
print(rows)
# [('ab',)]
conn.close()
```

Fix: always include the trailing comma — `("ab",)` — when passing a single parameter.

**Checking for missing values with `= NULL` instead of `IS NULL`.** In SQL, `NULL` means "unknown", so `col = NULL` is never true and silently returns zero rows:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE logs (user TEXT, note TEXT)")
with conn:
    conn.executemany(
        "INSERT INTO logs (user, note) VALUES (?, ?)",
        [("an", None), ("binh", "ok")],
    )

print(conn.execute("SELECT user FROM logs WHERE note = NULL ORDER BY user").fetchall())
# []
print(conn.execute("SELECT user FROM logs WHERE note IS NULL ORDER BY user").fetchall())
# [('an',)]
conn.close()
```

Fix: use `IS NULL` (or `IS NOT NULL`) whenever you test for SQL `NULL`.

**Forgetting `ORDER BY` when expecting a fixed row order.** A SQL table is an unordered set of rows: without `ORDER BY`, SQLite can return rows in any order, especially after deletions or updates. Always end multi-row `SELECT` queries with `ORDER BY` (and a tie-breaker column when needed) whenever order matters:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE evals (user TEXT, score REAL)")
with conn:
    conn.executemany(
        "INSERT INTO evals (user, score) VALUES (?, ?)",
        [("binh", 0.8), ("an", 0.9), ("chi", 0.9)],
    )

# Fixed: always add ORDER BY when row order matters
rows = conn.execute(
    "SELECT user, score FROM evals ORDER BY score DESC, user ASC"
).fetchall()
print(rows)
# [('an', 0.9), ('chi', 0.9), ('binh', 0.8)]
conn.close()
```

## Recap

- Open an in-memory database with `sqlite3.connect(":memory:")`, create tables with `CREATE TABLE`, and close connections with `conn.close()` when done.
- Insert rows safely inside `with conn:` using `?` placeholders (`execute` or `executemany`) — never f-strings, and remember the trailing comma in single-item tuples like `(x,)`.
- Query rows with `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT`, and read results with `.fetchall()` or `.fetchone()`.
- Summarise groups with `COUNT(*)`, `SUM`, `AVG`, `ROUND(..., 2)`, `GROUP BY`, and `HAVING`.
- Load pre-filtered SQL results into pandas with `pd.read_sql_query(sql, conn, params=(...,))`.
- Remember SQL's execution order (`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`), which is why `WHERE` filters rows before grouping and `HAVING` filters groups after.
