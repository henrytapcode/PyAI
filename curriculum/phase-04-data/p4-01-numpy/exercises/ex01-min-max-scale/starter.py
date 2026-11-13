import numpy as np


def min_max_scale(values: np.ndarray) -> np.ndarray:
    """Scale values into the [0, 1] range using (x - min) / (max - min).

    Example: min_max_scale(np.array([10, 20, 30])) returns array([0.0, 0.5, 1.0])
    """
    low = values.___()
    high = values.___()
    return (values - ___) / (high - ___)
