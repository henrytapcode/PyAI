import pytest
import torch

from exercise import fit_slope, slope_at


def test_slope_at_matches_exact_mse_gradient():
    xs = torch.tensor([1.0, 2.0, 3.0, 4.0])
    ys = torch.tensor([3.0, 6.0, 9.0, 12.0])
    w_test = 1.5
    expected = (2.0 * (w_test * xs - ys) * xs).mean().item()
    result = slope_at(w_test, xs, ys)
    assert result is not None, "slope_at returned None: did you forget to return the value?"
    assert result == pytest.approx(expected)


def test_slope_at_does_not_accumulate_across_calls():
    xs = torch.tensor([1.0, 2.0, 3.0])
    ys = torch.tensor([3.0, 6.0, 9.0])
    first = slope_at(1.0, xs, ys)
    second = slope_at(1.0, xs, ys)
    assert first is not None, "slope_at returned None: did you forget to return the value?"
    assert first == pytest.approx(-18.667)
    assert first == second, "calling slope_at twice with the same w_value must give the same slope"


def test_fit_slope_converges_near_three():
    xs = torch.tensor([1.0, 2.0, 3.0, 4.0])
    ys = 3.0 * xs
    w = fit_slope(xs, ys, lr=0.05, steps=20)
    assert w is not None, "fit_slope returned None: did you forget to return the value?"
    assert w == pytest.approx(3.0, abs=0.05)


def test_fit_slope_zero_steps_returns_zero():
    xs = torch.tensor([1.0, 2.0, 3.0])
    ys = 3.0 * xs
    w = fit_slope(xs, ys, lr=0.05, steps=0)
    assert w is not None, "fit_slope returned None: did you forget to return the value?"
    assert w == 0.0


def test_fit_slope_one_step_matches_exact_update():
    xs = torch.tensor([1.0, 2.0, 3.0, 4.0])
    ys = 3.0 * xs
    # At w=0.0, gradient = mean(-2 * 3 * xs^2) = -6 * 7.5 = -45.0 -> w = 0 - 0.05 * (-45.0) = 2.25
    w = fit_slope(xs, ys, lr=0.05, steps=1)
    assert w is not None, "fit_slope returned None: did you forget to return the value?"
    assert w == pytest.approx(2.25, abs=1e-6)


def test_both_functions_return_python_floats():
    xs = torch.tensor([1.0, 2.0, 3.0])
    ys = 3.0 * xs
    slope = slope_at(1.0, xs, ys)
    fitted = fit_slope(xs, ys, lr=0.05, steps=10)
    assert type(slope) is float, "slope_at must return a built-in Python float, not a tensor"
    assert type(fitted) is float, "fit_slope must return a built-in Python float, not a tensor"
