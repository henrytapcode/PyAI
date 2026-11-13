import numpy as np


def precision_recall_f1(
    y_true: np.ndarray, y_pred: np.ndarray
) -> tuple[float, float, float]:
    """Compute (precision, recall, f1) rounded to 3 decimals; return 0.0 on zero denominator.

    Example:
        precision_recall_f1(np.array([1, 1, 1, 0, 0]), np.array([1, 0, 0, 0, 0]))
        -> (1.0, 0.333, 0.5)
    """
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return (
        round(float(precision), 3),
        round(float(recall), 3),
        round(float(f1), 3),
    )


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
    for t in sorted(thresholds, reverse=True):
        preds = (probs >= t).astype("int64")
        tp = int(((y_true == 1) & (preds == 1)).sum())
        fn = int(((y_true == 1) & (preds == 0)).sum())
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        if recall >= min_recall:
            return float(t)
    return None
