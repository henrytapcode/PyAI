import sqlite3


def create_feedback_db(rows: list[tuple[str, str, int]]) -> sqlite3.Connection:
    """Create an in-memory feedback database and insert (user, model, rating) rows.

    Example: conn = create_feedback_db([("an", "mini", 2)])
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE feedback (
            user TEXT,
            model TEXT,
            rating INTEGER
        )
    """)
    with conn:
        conn.executemany(
            "INSERT INTO feedback (user, model, rating) VALUES (?, ?, ?)",
            rows,
        )
    return conn


def low_rated_users(conn: sqlite3.Connection, max_rating: int) -> list[str]:
    """Return sorted unique users with at least one rating <= max_rating.

    Example: low_rated_users(conn, 2) -> ["an"]
    """
    rows = conn.execute(
        """
        SELECT DISTINCT user
        FROM feedback
        WHERE rating <= ?
        ORDER BY user ASC
        """,
        (max_rating,),
    ).fetchall()
    return [row[0] for row in rows]
