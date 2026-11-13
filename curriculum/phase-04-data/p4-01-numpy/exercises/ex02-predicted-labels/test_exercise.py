import numpy as np

from exercise import predicted_labels


def test_predicts_labels_and_marks_low_confidence_unsure():
    probs = np.array([
        [0.05, 0.15, 0.80],
        [0.50, 0.30, 0.20],
        [0.10, 0.75, 0.15],
    ])
    result = predicted_labels(probs, ["neg", "neu", "pos"], 0.7)
    assert result == ["pos", "unsure", "neu"]


def test_returns_python_list_of_strings():
    probs = np.array([[0.9, 0.1]])
    result = predicted_labels(probs, ["a", "b"], 0.5)
    assert type(result) is list, "return a plain Python list, not a NumPy array"
    assert all(isinstance(item, str) for item in result)


def test_accepts_probability_equal_to_threshold():
    probs = np.array([[0.60, 0.40], [0.59, 0.41]])
    result = predicted_labels(probs, ["yes", "no"], 0.6)
    assert result == ["yes", "unsure"], "exact threshold (prob == threshold) should be accepted"


def test_breaks_ties_using_first_class_index():
    probs = np.array([
        [0.50, 0.50, 0.00],
        [0.10, 0.45, 0.45],
    ])
    result = predicted_labels(probs, ["first", "second", "third"], 0.4)
    assert result == ["first", "second"], "argmax picks the lowest index on a tie"


def test_handles_empty_batch_and_does_not_mutate_inputs():
    empty = np.empty((0, 3))
    labels = ["a", "b", "c"]
    assert predicted_labels(empty, labels, 0.5) == []

    probs = np.array([[0.2, 0.8]])
    snapshot = probs.copy()
    predicted_labels(probs, labels, 0.5)
    assert probs.tolist() == snapshot.tolist()
    assert labels == ["a", "b", "c"]
