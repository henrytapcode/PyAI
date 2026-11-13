import sqlite3


def create_feedback_db(rows: list[tuple[str, str, int]]) -> sqlite3.Connection:
    """Create an in-memory feedback database and insert (user, model, rating) rows.

    Example: conn = create_feedback_db([("an", "mini", 2)])
    """
    # TODO: open sqlite3.connect(":memory:"), create table feedback, insert rows with ?
    pass


def low_rated_users(conn: sqlite3.Connection, max_rating: int) -> list[str]:
    """Return sorted unique users with at least one rating <= max_rating.

    Example: low_rated_users(conn, 2) -> ["an"]
    """
    # TODO: query feedback using a ? placeholder for max_rating and return sorted names
    pass
