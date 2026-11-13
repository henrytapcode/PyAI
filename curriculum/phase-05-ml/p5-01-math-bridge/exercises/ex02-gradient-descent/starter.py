import numpy as np


def mse(w: float, b: float, xs: np.ndarray, ys: np.ndarray) -> float:
    """Return the mean squared error of w * xs + b against ys as a Python float.

    Example: mse(2.0, 1.0, np.array([1.0, 2.0]), np.array([3.0, 5.0])) returns 0.0
    """
    # TODO: compute predictions w * xs + b and return float(np.mean((pred - ys) ** 2))
    return 0.0


def fit_line(xs: np.ndarray, ys: np.ndarray, lr: float, steps: int) -> tuple[float, float]:
    """Fit y = w * x + b from w=0.0, b=0.0 with gradient descent and return (w, b).

    Example: fit_line(np.array([1.0, 2.0, 3.0, 4.0]), np.array([3.0, 5.0, 7.0, 9.0]), 0.05, 250)
    returns approximately (2.0, 1.0)
    """
    # TODO: initialise w = 0.0 and b = 0.0
    # TODO: loop `steps` times, compute grad_w and grad_b, and step downhill by lr
    # TODO: return (round(float(w), 3), round(float(b), 3))
    return (0.0, 0.0)
