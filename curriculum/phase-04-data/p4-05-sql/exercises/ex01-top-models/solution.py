import sqlite3


def top_models(conn: sqlite3.Connection, min_runs: int) -> list[tuple[str, float]]:
    """Return (model, avg_score) for models with at least min_runs rows.

    Example: top_models(conn, 2) -> [("gpt-4o", 0.9), ("claude", 0.88)]
    """
    sql = """
        SELECT model, ROUND(AVG(score), 2) AS avg_score
        FROM runs
        GROUP BY model
        HAVING COUNT(*) >= ?
        ORDER BY avg_score DESC, model ASC
    """
    return conn.execute(sql, (min_runs,)).fetchall()
