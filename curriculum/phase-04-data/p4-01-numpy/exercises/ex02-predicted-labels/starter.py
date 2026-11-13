import numpy as np


def predicted_labels(probs: np.ndarray, labels: list[str], threshold: float) -> list[str]:
    """Return the predicted label for each row of probs, or "unsure" if below threshold.

    Example: predicted_labels(np.array([[0.1, 0.9], [0.55, 0.45]]), ["no", "yes"], 0.6)
    returns ["yes", "unsure"]
    """
    # TODO 1: find the winning class index for each row using axis=1
    # TODO 2: find the highest probability for each row using axis=1
    # TODO 3: build and return a Python list of label strings (or "unsure" if < threshold)
    return []
