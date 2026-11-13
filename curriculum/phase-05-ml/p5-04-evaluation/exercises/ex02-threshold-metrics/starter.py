import numpy as np


def precision_recall_f1(
    y_true: np.ndarray, y_pred: np.ndarray
) -> tuple[float, float, float]:
    """Compute (precision, recall, f1) rounded to 3 decimals; return 0.0 on zero denominator.

    Example:
        precision_recall_f1(np.array([1, 1, 1, 0, 0]), np.array([1, 0, 0, 0, 0]))
        -> (1.0, 0.333, 0.5)
    """
    # TODO: count tp, fp, fn using NumPy boolean comparisons
    # TODO: compute precision, recall, and f1 safely (0.0 on zero denominator)
    # TODO: round each value to 3 decimal places as plain Python floats
    return (0.0, 0.0, 0.0)


def threshold_for_recall(
    probs: np.ndarray,
    y_true: np.ndarray,
    thresholds: list[float],
    min_recall: float,
) -> float | None:
    """Return the largest threshold where recall >= min_recall, or None if none qualifies.

    Example:
        threshold_for_recall(
            np.array([0.8, 0.4, 0.2]),
            np.array([1, 1, 0]),
            [0.3, 0.5, 0.7],
            0.8,
        ) -> 0.3
    """
    # TODO: test each threshold t in thresholds with preds = (probs >= t).astype("int64")
    # TODO: compute recall and return the largest t with recall >= min_recall (else None)
    return None
