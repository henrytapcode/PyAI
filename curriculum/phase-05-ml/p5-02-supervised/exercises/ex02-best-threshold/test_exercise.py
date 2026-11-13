import numpy as np
import pytest

from exercise import accuracy, best_threshold


def test_accuracy_computes_correct_fraction():
    preds = np.array([0, 1, 1, 0, 1])
    labels = np.array([0, 1, 0, 0, 1])
    assert accuracy(preds, labels) == pytest.approx(0.8)


def test_accuracy_returns_zero_for_empty_array():
    empty = np.array([], dtype="int64")
    assert accuracy(empty, empty) == 0.0


def test_best_threshold_perfect_separation():
    scores = np.array([0.85, 0.15, 0.65, 0.25, 0.92, 0.10])
    labels = np.array([1, 0, 1, 0, 1, 0])
    t, acc = best_threshold(scores, labels)
    assert t == pytest.approx(0.65)
    assert acc == 1.0


def test_best_threshold_picks_smallest_on_tie():
    scores = np.array([0.2, 0.5, 0.5, 0.8])
    labels = np.array([0, 1, 0, 1])
    t, acc = best_threshold(scores, labels)
    assert t == pytest.approx(0.5), "on a tie (0.5 and 0.8 both give 0.75), pick the smallest t"
    assert acc == 0.75


def test_return_types_are_python_floats():
    scores = np.array([0.3, 0.6, 0.9])
    labels = np.array([0, 1, 1])
    acc_single = accuracy(np.array([0, 1, 1]), labels)
    t, acc = best_threshold(scores, labels)
    assert type(acc_single) is float, "accuracy must return a built-in Python float"
    assert type(t) is float, "threshold must be a built-in Python float"
    assert type(acc) is float, "best accuracy must be a built-in Python float"


def test_does_not_modify_input_arrays():
    scores = np.array([0.9, 0.1, 0.4, 0.7])
    labels = np.array([1, 0, 0, 1])
    scores_copy = scores.copy()
    labels_copy = labels.copy()
    best_threshold(scores, labels)
    assert np.array_equal(scores, scores_copy)
    assert np.array_equal(labels, labels_copy)
