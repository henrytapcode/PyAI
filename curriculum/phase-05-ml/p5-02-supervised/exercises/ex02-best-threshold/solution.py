import numpy as np


def accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
    """Return the fraction of matching labels as a Python float, or 0.0 if empty.

    Example: accuracy(np.array([0, 1, 1]), np.array([0, 0, 1])) returns 0.6666666666666666
    """
    if len(preds) == 0:
        return 0.0
    return float((preds == labels).mean())


def best_threshold(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    """Find the threshold t from scores giving highest accuracy (smallest t on ties).

    Example: best_threshold(np.array([0.1, 0.4, 0.7, 0.9]), np.array([0, 0, 1, 1]))
    returns (0.7, 1.0)
    """
    if len(scores) == 0:
        return (0.0, 0.0)
    best_t = 0.0
    best_acc = -1.0
    for t in np.unique(scores):
        preds = (scores >= t).astype("int64")
        acc = accuracy(preds, labels)
        if acc > best_acc:
            best_acc = acc
            best_t = float(t)
    return (float(best_t), round(float(best_acc), 3))
