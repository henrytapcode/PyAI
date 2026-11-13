import sqlite3

import pytest

from exercise import top_models


@pytest.fixture
def runs_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE runs (model TEXT, score REAL)")
    with conn:
        conn.executemany(
            "INSERT INTO runs (model, score) VALUES (?, ?)",
            [
                ("gpt-4o", 0.92),
                ("gpt-4o", 0.88),
                ("claude", 0.80),
                ("claude", 0.90),
                ("claude", 0.80),
                ("zeta", 0.85),
                ("zeta", 0.85),
                ("alpha", 0.85),
                ("alpha", 0.85),
                ("mini", 0.99),
            ],
        )
    yield conn
    conn.close()


def test_excludes_models_below_min_runs(runs_conn):
    result = top_models(runs_conn, 2)
    models = [model for model, _ in result]
    assert "mini" not in models, (
        "models with fewer than min_runs rows must be filtered out by HAVING"
    )


def test_includes_models_at_exact_min_runs_boundary(runs_conn):
    result = top_models(runs_conn, 3)
    assert result == [("claude", 0.83)]


def test_orders_descending_by_average_and_breaks_ties_alphabetically(runs_conn):
    result = top_models(runs_conn, 2)
    assert result == [
        ("gpt-4o", 0.9),
        ("alpha", 0.85),
        ("zeta", 0.85),
        ("claude", 0.83),
    ]


def test_rounds_average_score_to_two_decimals(runs_conn):
    result = dict(top_models(runs_conn, 2))
    assert result["claude"] == 0.83


def test_returns_empty_list_when_no_model_meets_min_runs(runs_conn):
    assert top_models(runs_conn, 10) == []
