import numpy as np
import pytest
from sklearn.metrics import confusion_matrix

from exercise import confusion_counts


def test_returns_expected_counts_on_fixed_arrays():
    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_pred = np.array([0, 1, 0, 0, 1, 1])
    assert confusion_counts(y_true, y_pred) == {"tp": 2, "fp": 1, "fn": 1, "tn": 2}


def test_values_are_plain_python_ints():
    y_true = np.array([1, 1, 0, 0])
    y_pred = np.array([1, 0, 1, 0])
    counts = confusion_counts(y_true, y_pred)
    assert set(counts.keys()) == {"tp", "fp", "fn", "tn"}
    assert all(type(v) is int for v in counts.values()), (
        "every count must be a plain Python int, not a NumPy scalar"
    )


def test_counts_sum_to_total_samples():
    y_true = np.array([0, 1, 0, 1, 1, 0, 0, 1, 0])
    y_pred = np.array([0, 0, 1, 1, 1, 0, 1, 0, 0])
    counts = confusion_counts(y_true, y_pred)
    assert sum(counts.values()) == len(y_true)


@pytest.mark.parametrize(
    ("y_true", "y_pred"),
    [
        (np.array([0, 0, 0, 1, 1]), np.array([0, 1, 0, 0, 1])),
        (np.array([1, 0, 1, 0, 1, 0]), np.array([0, 1, 1, 0, 0, 1])),
    ],
)
def test_matches_sklearn_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray):
    counts = confusion_counts(y_true, y_pred)
    expected_tn, expected_fp, expected_fn, expected_tp = (
        confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel().tolist()
    )
    assert [counts["tn"], counts["fp"], counts["fn"], counts["tp"]] == [
        expected_tn,
        expected_fp,
        expected_fn,
        expected_tp,
    ]


def test_all_zeros_and_all_ones():
    zeros = np.array([0, 0, 0, 0])
    ones = np.array([1, 1, 1, 1])
    assert confusion_counts(zeros, zeros) == {"tp": 0, "fp": 0, "fn": 0, "tn": 4}
    assert confusion_counts(ones, ones) == {"tp": 4, "fp": 0, "fn": 0, "tn": 0}
    assert confusion_counts(ones, zeros) == {"tp": 0, "fp": 0, "fn": 4, "tn": 0}


def test_does_not_modify_input_arrays():
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([1, 1, 0, 0])
    y_true_copy = y_true.copy()
    y_pred_copy = y_pred.copy()
    confusion_counts(y_true, y_pred)
    assert np.array_equal(y_true, y_true_copy)
    assert np.array_equal(y_pred, y_pred_copy)
