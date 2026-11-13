import numpy as np


def predicted_labels(probs: np.ndarray, labels: list[str], threshold: float) -> list[str]:
    """Return the predicted label for each row of probs, or "unsure" if below threshold."""
    result: list[str] = []
    for row in probs:
        best_idx = int(row.argmax())
        if row[best_idx] < threshold:
            result.append("unsure")
        else:
            result.append(labels[best_idx])
    return result
