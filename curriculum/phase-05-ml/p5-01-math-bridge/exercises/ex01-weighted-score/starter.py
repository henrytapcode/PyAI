import numpy as np


def weighted_score(features: np.ndarray, weights: np.ndarray, bias: float) -> float:
    """Return the weighted score as a Python float: features @ weights + bias.

    Example: weighted_score(np.array([2.0, 3.0]), np.array([0.5, 1.0]), 0.5) returns 4.5
    """
    dot = np.___(features, weights)
    total = dot + ___
    return ___(total)
