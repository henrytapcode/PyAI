import numpy as np


def accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
    """Return the fraction of matching labels as a Python float, or 0.0 if empty.

    Example: accuracy(np.array([0, 1, 1]), np.array([0, 0, 1])) returns 0.6666666666666666
    """
    # TODO: return 0.0 when preds is empty, otherwise the matching fraction as a Python float
    return 0.0


def best_threshold(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    """Find the threshold t from scores giving highest accuracy (smallest t on ties).

    Example: best_threshold(np.array([0.1, 0.4, 0.7, 0.9]), np.array([0, 0, 1, 1]))
    returns (0.7, 1.0)
    """
    # TODO: try each distinct value in scores, predict 1 if score >= t else 0
    # TODO: return (float(best_t), round(float(best_acc), 3))
    return (0.0, 0.0)
