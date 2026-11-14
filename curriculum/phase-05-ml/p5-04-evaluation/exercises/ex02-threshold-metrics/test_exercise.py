import numpy as np
import pytest
from sklearn.metrics import f1_score, precision_score, recall_score

from exercise import precision_recall_f1, threshold_for_recall


@pytest.mark.parametrize(
    ("y_true", "y_pred"),
    [
        (np.array([1, 1, 1, 0, 0]), np.array([1, 0, 0, 0, 0])),
        (np.array([0, 0, 0, 1, 1, 1]), np.array([0, 1, 0, 0, 1, 1])),
        (np.array([1, 0, 1, 0, 1, 1]), np.array([1, 1, 0, 0, 1, 0])),
    ],
)
def test_precision_recall_f1_matches_sklearn(y_true: np.ndarray, y_pred: np.ndarray):
    result = precision_recall_f1(y_true, y_pred)
    assert len(result) == 3
    assert all(type(v) is float for v in result), "return plain Python floats"
    expected = (
        round(float(precision_score(y_true, y_pred, zero_division=0)), 3),
        round(float(recall_score(y_true, y_pred, zero_division=0)), 3),
        round(float(f1_score(y_true, y_pred, zero_division=0)), 3),
    )
    assert result == expected


def test_precision_recall_f1_zero_denominators():
    # No positive predictions (tp + fp == 0)
    assert precision_recall_f1(np.array([0, 1, 1]), np.array([0, 0, 0])) == (0.0, 0.0, 0.0)
    # No actual positives (tp + fn == 0)
    assert precision_recall_f1(np.array([0, 0, 0]), np.array([1, 0, 0])) == (0.0, 0.0, 0.0)
    # False positives and false negatives, zero true positives (precision + recall == 0)
    assert precision_recall_f1(np.array([1, 0]), np.array([0, 1])) == (0.0, 0.0, 0.0)


def test_threshold_for_recall_picks_largest_qualifying():
    probs = np.array([0.85, 0.62, 0.35, 0.15])
    y_true = np.array([1, 1, 1, 0])
    chosen = threshold_for_recall(probs, y_true, [0.2, 0.3, 0.5, 0.7], min_recall=0.65)
    assert type(chosen) is float
    assert chosen == 0.5, "0.2, 0.3, and 0.5 all give recall >= 0.65; pick the largest (0.5)"


def test_threshold_for_recall_handles_unsorted_thresholds():
    probs = np.array([0.9, 0.45, 0.35, 0.1])
    y_true = np.array([1, 1, 0, 0])
    chosen = threshold_for_recall(probs, y_true, [0.2, 0.8, 0.4, 0.6], min_recall=0.9)
    assert chosen == 0.4, "sort or track max so unsorted thresholds still return the largest match"


def test_threshold_for_recall_returns_none_when_unreachable():
    probs = np.array([0.8, 0.2, 0.1])
    y_true = np.array([1, 1, 0])
    assert threshold_for_recall(probs, y_true, [0.3, 0.5, 0.7], min_recall=0.9) is None
    assert threshold_for_recall(probs, y_true, [], min_recall=0.5) is None


def test_does_not_modify_inputs():
    probs = np.array([0.8, 0.4, 0.2])
    y_true = np.array([1, 1, 0])
    thresholds = [0.5, 0.2, 0.7]
    probs_copy = probs.copy()
    y_true_copy = y_true.copy()
    thresholds_copy = list(thresholds)

    precision_recall_f1(y_true, (probs >= 0.5).astype("int64"))
    threshold_for_recall(probs, y_true, thresholds, 0.5)

    assert np.array_equal(probs, probs_copy)
    assert np.array_equal(y_true, y_true_copy)
    assert thresholds == thresholds_copy
