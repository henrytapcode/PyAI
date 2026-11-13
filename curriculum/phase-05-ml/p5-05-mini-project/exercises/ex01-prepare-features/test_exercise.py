import numpy as np
import pandas as pd
import pytest

from exercise import prepare_features


@pytest.fixture
def sample_raw() -> pd.DataFrame:
    return pd.DataFrame({
        "ticket_id": ["t01", "t02", "t02", "t03", "t04", "t05", "t06"],
        "plan": [" Free", "pro", "PRO", "Enterprise ", "free", "pro", "enterprise"],
        "tokens": ["1,200", "450", "999", "800", None, "300", "1,050"],
        "error_count": [2.0, 0.0, 5.0, 1.0, 1.0, float("nan"), 3.0],
        "hours_since_deploy": [4.5, 18.0, 1.0, 6.0, 12.0, 9.0, 2.0],
        "escalated_to_oncall": [1, 0, 1, 1, 0, 0, 1],
        "urgent": [1, 0, 1, 0, 0, 0, 1],
    })


def test_does_not_modify_input_dataframe(sample_raw: pd.DataFrame):
    snapshot = sample_raw.copy(deep=True)
    prepare_features(sample_raw)
    pd.testing.assert_frame_equal(sample_raw, snapshot)


def test_returns_exact_feature_column_order_and_dtypes(sample_raw: pd.DataFrame):
    X, y = prepare_features(sample_raw)
    assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray)
    assert X.ndim == 2 and X.shape == (4, 4)
    assert y.ndim == 1 and y.shape == (4,)
    assert str(X.dtype) == "float64"
    assert str(y.dtype) == "int64"
    # First surviving row is t01: tokens=1200, error_count=2, hours=4.5, plan=free (0.0)
    assert X[0].tolist() == pytest.approx([1200.0, 2.0, 4.5, 0.0])


def test_normalises_messy_plan_names_and_drops_unknown_plans():
    df = pd.DataFrame({
        "ticket_id": ["a1", "a2", "a3", "a4"],
        "plan": [" FREE ", "Pro", "ENTERPRISE ", "vip"],
        "tokens": ["100", "200", "300", "400"],
        "error_count": [0, 1, 2, 3],
        "hours_since_deploy": [5.0, 6.0, 7.0, 8.0],
        "escalated_to_oncall": [0, 0, 1, 1],
        "urgent": [0, 0, 1, 1],
    })
    X, y = prepare_features(df)
    assert X.shape == (3, 4), "unknown plan 'vip' should be dropped"
    assert X[:, 3].tolist() == pytest.approx([0.0, 1.0, 2.0])
    assert y.tolist() == [0, 0, 1]


def test_parses_comma_tokens_and_coerces_bad_numbers():
    df = pd.DataFrame({
        "ticket_id": ["a1", "a2", "a3"],
        "plan": ["free", "pro", "enterprise"],
        "tokens": ["1,500", "bad", "2,050"],
        "error_count": [1, 2, "oops"],
        "hours_since_deploy": [3.0, 4.0, 5.0],
        "escalated_to_oncall": [0, 1, 1],
        "urgent": [0, 1, 1],
    })
    X, y = prepare_features(df)
    assert X.shape == (1, 4)
    assert X[0, 0] == pytest.approx(1500.0)
    assert y.tolist() == [0]


def test_drops_duplicate_ticket_ids_keeping_first(sample_raw: pd.DataFrame):
    X, y = prepare_features(sample_raw)
    # t02 appears twice; keeping first preserves tokens=450, error_count=0, urgent=0
    assert X[1].tolist() == pytest.approx([450.0, 0.0, 18.0, 1.0])
    assert int(y[1]) == 0


def test_drops_rows_with_missing_numeric_features(sample_raw: pd.DataFrame):
    X, y = prepare_features(sample_raw)
    assert len(X) == len(y) == 4, "t04 (missing tokens) and t05 (NaN error_count) must be dropped"
    assert not np.isnan(X).any()


def test_excludes_leakage_column_even_when_present():
    df_a = pd.DataFrame({
        "ticket_id": ["t1", "t2"],
        "plan": ["free", "pro"],
        "tokens": ["100", "200"],
        "error_count": [0.0, 2.0],
        "hours_since_deploy": [10.0, 2.0],
        "escalated_to_oncall": [0, 1],
        "urgent": [0, 1],
    })
    df_b = df_a.copy()
    df_b["escalated_to_oncall"] = [1, 0]
    X_a, _ = prepare_features(df_a)
    X_b, _ = prepare_features(df_b)
    assert X_a.shape[1] == 4, "X must have only 4 features (never include escalated_to_oncall)"
    assert np.array_equal(X_a, X_b), "changing escalated_to_oncall must not change X"


def test_y_contains_only_zero_and_one(sample_raw: pd.DataFrame):
    _, y = prepare_features(sample_raw)
    assert set(y.tolist()).issubset({0, 1})
    assert y.tolist() == [1, 0, 0, 1]


def test_returns_empty_arrays_with_four_columns_when_all_rows_invalid():
    df_bad = pd.DataFrame({
        "ticket_id": ["t1", "t2"],
        "plan": ["unknown", "free"],
        "tokens": ["100", None],
        "error_count": [1.0, 2.0],
        "hours_since_deploy": [5.0, 5.0],
        "escalated_to_oncall": [0, 1],
        "urgent": [0, 1],
    })
    X, y = prepare_features(df_bad)
    assert X.shape == (0, 4)
    assert y.shape == (0,)
    assert str(X.dtype) == "float64"
    assert str(y.dtype) == "int64"
