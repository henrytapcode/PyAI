import numpy as np
import pytest

from exercise import weighted_score


def test_computes_weighted_score():
    features = np.array([2.0, 3.0, 4.0])
    weights = np.array([0.5, 1.0, -0.25])
    result = weighted_score(features, weights, 1.0)
    assert result == pytest.approx(4.0)


def test_returns_python_float():
    result = weighted_score(np.array([1.0, 2.0]), np.array([0.5, 0.5]), 0.0)
    assert type(result) is float, "wrap the result in float(...) so it is not a NumPy scalar"


def test_handles_negative_bias():
    features = np.array([4.0, 2.0])
    weights = np.array([0.5, 1.5])
    result = weighted_score(features, weights, -6.5)
    assert result == pytest.approx(-1.5)


def test_zero_weights_returns_bias():
    features = np.array([10.0, -3.5, 7.0])
    weights = np.array([0.0, 0.0, 0.0])
    result = weighted_score(features, weights, 2.25)
    assert result == pytest.approx(2.25)
