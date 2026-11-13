import numpy as np


def mse(w: float, b: float, xs: np.ndarray, ys: np.ndarray) -> float:
    """Return the mean squared error of w * xs + b against ys as a Python float."""
    pred = w * xs + b
    return float(np.mean((pred - ys) ** 2))


def fit_line(xs: np.ndarray, ys: np.ndarray, lr: float, steps: int) -> tuple[float, float]:
    """Fit y = w * x + b by estimating the slope of mse numerically around (w, b)."""
    w = 0.0
    b = 0.0
    h = 0.001
    for _ in range(steps):
        slope_w = (mse(w + h, b, xs, ys) - mse(w - h, b, xs, ys)) / (2 * h)
        slope_b = (mse(w, b + h, xs, ys) - mse(w, b - h, xs, ys)) / (2 * h)
        w = w - lr * slope_w
        b = b - lr * slope_b
    return (round(float(w), 3), round(float(b), 3))
