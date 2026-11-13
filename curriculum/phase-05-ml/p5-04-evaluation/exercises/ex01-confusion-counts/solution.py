import numpy as np


def confusion_counts(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    """Count TP, FP, FN, and TN as plain Python ints from binary 0/1 arrays.

    Example:
        confusion_counts(np.array([1, 1, 0, 0]), np.array([1, 0, 1, 0]))
        -> {'tp': 1, 'fp': 1, 'fn': 1, 'tn': 1}
    """
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
