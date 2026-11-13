import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score


def precision_recall_f1(
    y_true: np.ndarray, y_pred: np.ndarray
) -> tuple[float, float, float]:
    """Compute (precision, recall, f1) using scikit-learn metrics with zero_division=0."""
    return (
        round(float(precision_score(y_true, y_pred, zero_division=0)), 3),
        round(float(recall_score(y_true, y_pred, zero_division=0)), 3),
        round(float(f1_score(y_true, y_pred, zero_division=0)), 3),
    )


def threshold_for_recall(
    probs: np.ndarray,
    y_true: np.ndarray,
    thresholds: list[float],
    min_recall: float,
) -> float | None:
    """Pick the largest threshold meeting min_recall using sklearn recall_score."""
    qualifying = [
        float(t)
        for t in thresholds
        if float(recall_score(y_true, (probs >= t).astype("int64"), zero_division=0))
        >= min_recall
    ]
    return max(qualifying) if qualifying else None
