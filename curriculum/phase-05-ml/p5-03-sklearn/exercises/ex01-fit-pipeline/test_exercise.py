import numpy as np
import pytest
from sklearn.datasets import load_iris

from exercise import train_and_score


def test_returns_python_float():
    X, y = load_iris(return_X_y=True)
    score = train_and_score(X, y, seed=42)
    assert type(score) is float, "return a plain Python float, not a NumPy scalar"


def test_expected_score_on_fixed_dataset():
    X, y = load_iris(return_X_y=True)
    score = train_and_score(X, y, seed=42)
    assert score == 0.921, (
        "check test_size=0.25, stratify=y, StandardScaler, and rounding to 3 decimals"
    )


def test_same_seed_gives_identical_score():
    X, y = load_iris(return_X_y=True)
    first = train_and_score(X, y, seed=7)
    second = train_and_score(X, y, seed=7)
    assert first == second


@pytest.mark.parametrize("seed", [0, 7, 42])
def test_different_seeds_stay_in_unit_interval(seed: int):
    X, y = load_iris(return_X_y=True)
    score = train_and_score(X, y, seed=seed)
    assert 0.0 <= score <= 1.0


def test_does_not_modify_input_arrays():
    X, y = load_iris(return_X_y=True)
    X_copy = X.copy()
    y_copy = y.copy()
    train_and_score(X, y, seed=42)
    assert np.array_equal(X, X_copy)
    assert np.array_equal(y, y_copy)
