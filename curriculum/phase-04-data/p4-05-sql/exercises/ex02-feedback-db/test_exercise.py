import sqlite3

import pytest

from exercise import create_feedback_db, low_rated_users


@pytest.fixture
def sample_conn():
    conn = create_feedback_db([
        ("binh", "mini", 2),
        ("an", "gpt-4o", 5),
        ("an", "mini", 1),
        ("binh", "claude", 1),
        ("chi", "gpt-4o", 4),
        ("dung", "mini", 3),
    ])
    yield conn
    conn.close()


def test_creates_feedback_table_and_inserts_all_rows(sample_conn):
    assert isinstance(sample_conn, sqlite3.Connection)
    count = sample_conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    assert count == 6


def test_handles_apostrophes_with_parameterized_insert():
    conn = create_feedback_db([
        ("O'Brien", "gpt-4o", 1),
        ("an", "mini", 5),
    ])
    try:
        assert low_rated_users(conn, 2) == ["O'Brien"]
    finally:
        conn.close()


def test_returns_unique_sorted_users_without_duplicates(sample_conn):
    assert low_rated_users(sample_conn, 2) == ["an", "binh"]


def test_includes_boundary_rating_equal_to_max_rating(sample_conn):
    assert low_rated_users(sample_conn, 3) == ["an", "binh", "dung"]


def test_returns_empty_list_for_empty_database():
    conn = create_feedback_db([])
    try:
        assert low_rated_users(conn, 5) == []
    finally:
        conn.close()


def test_returns_empty_list_when_no_rating_is_low_enough(sample_conn):
    assert low_rated_users(sample_conn, 0) == []
