import sqlite3


def top_models(conn: sqlite3.Connection, min_runs: int) -> list[tuple[str, float]]:
    """Return (model, avg_score) for models with at least min_runs rows.

    Example: top_models(conn, 2) -> [("gpt-4o", 0.9), ("mini", 0.75)]
    """
    sql = """
        SELECT model, ROUND(AVG(score), ___) AS avg_score
        FROM runs
        GROUP BY ___
        HAVING COUNT(*) >= ___
        ORDER BY ___ DESC, model ASC
    """
    return conn.execute(sql, (min_runs,)).fetchall()
