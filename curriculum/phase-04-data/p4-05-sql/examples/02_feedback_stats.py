# Aggregate model ratings with GROUP BY and HAVING, then print rounded averages.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE feedback (
        id INTEGER PRIMARY KEY,
        model TEXT,
        rating INTEGER
    )
""")

rows = [
    ("gpt-4o", 5),
    ("mini", 3),
    ("gpt-4o", 4),
    ("claude", 5),
    ("mini", 4),
    ("claude", 4),
    ("local-7b", 2),
]
with conn:
    conn.executemany(
        "INSERT INTO feedback (model, rating) VALUES (?, ?)",
        rows,
    )

stats = conn.execute("""
    SELECT
        model,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS n_ratings
    FROM feedback
    GROUP BY model
    HAVING COUNT(*) >= 2
    ORDER BY avg_rating DESC, model ASC
""").fetchall()

for model, avg_rating, n_ratings in stats:
    print(f"{model}: {avg_rating} ({n_ratings} ratings)")

conn.close()
