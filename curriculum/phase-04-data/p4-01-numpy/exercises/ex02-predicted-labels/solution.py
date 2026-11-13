import numpy as np


def predicted_labels(probs: np.ndarray, labels: list[str], threshold: float) -> list[str]:
    """Return the predicted label for each row of probs, or "unsure" if below threshold.

    Example: predicted_labels(np.array([[0.1, 0.9], [0.55, 0.45]]), ["no", "yes"], 0.6)
    returns ["yes", "unsure"]
    """
    best_ids = probs.argmax(axis=1)
    best_probs = probs.max(axis=1)
    return [
        labels[int(idx)] if prob >= threshold else "unsure"
        for idx, prob in zip(best_ids, best_probs, strict=True)
    ]
