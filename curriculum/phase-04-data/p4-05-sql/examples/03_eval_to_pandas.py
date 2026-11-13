# Load filtered eval runs from SQLite into pandas and compute mean score by model.
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE eval_runs (
        id INTEGER PRIMARY KEY,
        model TEXT,
        task TEXT,
        score REAL
    )
""")

runs = [
    ("gpt-4o", "qa", 0.92),
    ("gpt-4o", "summary", 0.88),
    ("claude", "qa", 0.90),
    ("claude", "summary", 0.86),
    ("mini", "qa", 0.78),
    ("mini", "summary", 0.74),
]
with conn:
    conn.executemany(
        "INSERT INTO eval_runs (model, task, score) VALUES (?, ?, ?)",
        runs,
    )

sql = """
    SELECT model, task, score
    FROM eval_runs
    WHERE score >= ?
    ORDER BY score DESC, model ASC
"""
df = pd.read_sql_query(sql, conn, params=(0.75,))
summary = (
    df.groupby("model")["score"]
    .mean()
    .reset_index()
    .round(2)
    .sort_values(by=["score", "model"], ascending=[False, True])
    .reset_index(drop=True)
)
print(summary)

conn.close()
