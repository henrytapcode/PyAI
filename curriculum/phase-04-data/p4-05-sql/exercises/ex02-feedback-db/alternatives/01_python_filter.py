import sqlite3


def create_feedback_db(rows: list[tuple[str, str, int]]) -> sqlite3.Connection:
    """Create an in-memory feedback database and insert (user, model, rating) rows."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE feedback (user TEXT, model TEXT, rating INTEGER)")
    with conn:
        for row in rows:
            conn.execute(
                "INSERT INTO feedback (user, model, rating) VALUES (?, ?, ?)",
                row,
            )
    return conn


def low_rated_users(conn: sqlite3.Connection, max_rating: int) -> list[str]:
    """Fetch all rows from SQLite, then deduplicate and sort in Python."""
    all_rows = conn.execute("SELECT user, rating FROM feedback").fetchall()
    matched = {user for user, rating in all_rows if rating <= max_rating}
    return sorted(matched)
