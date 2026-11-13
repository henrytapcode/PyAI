import numpy as np
import pytest

from exercise import fit_line, mse


def test_mse_is_zero_when_line_matches_all_points():
    xs = np.array([1.0, 2.0, 3.0, 4.0])
    ys = np.array([3.0, 5.0, 7.0, 9.0])
    assert mse(2.0, 1.0, xs, ys) == pytest.approx(0.0)


def test_mse_computes_mean_squared_error_as_python_float():
    xs = np.array([1.0, 2.0])
    ys = np.array([2.0, 5.0])
    # Predictions [1.0, 2.0], errors [-1.0, -3.0], squares [1.0, 9.0] -> mean 5.0
    loss = mse(1.0, 0.0, xs, ys)
    assert type(loss) is float, "mse must return a Python float, not a NumPy scalar"
    assert loss == pytest.approx(5.0)


def test_fit_line_converges_on_clean_linear_data():
    xs = np.array([1.0, 2.0, 3.0, 4.0])
    ys = 2.0 * xs + 1.0
    w, b = fit_line(xs, ys, lr=0.05, steps=250)
    assert (w, b) == pytest.approx((2.0, 1.0), abs=0.05)


def test_fit_line_zero_steps_returns_initial_zeros():
    xs = np.array([1.0, 2.0, 3.0])
    ys = np.array([3.0, 5.0, 7.0])
    assert fit_line(xs, ys, lr=0.05, steps=0) == (0.0, 0.0)


def test_fit_line_reduces_loss():
    xs = np.array([1.0, 2.0, 3.0, 4.0])
    ys = np.array([2.8, 5.1, 6.9, 9.2])
    start_loss = mse(0.0, 0.0, xs, ys)
    w, b = fit_line(xs, ys, lr=0.05, steps=50)
    end_loss = mse(w, b, xs, ys)
    assert end_loss < start_loss, "loss after fitting must be smaller than starting loss"


def test_fit_line_returns_tuple_of_two_python_floats():
    xs = np.array([1.0, 2.0, 3.0])
    ys = np.array([2.0, 4.0, 6.0])
    result = fit_line(xs, ys, lr=0.05, steps=20)
    assert isinstance(result, tuple) and len(result) == 2
    assert type(result[0]) is float and type(result[1]) is float, "return built-in Python floats"
