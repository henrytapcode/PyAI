import numpy as np


def accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
    """Return the fraction of matching labels using a pure Python loop."""
    if len(preds) == 0:
        return 0.0
    matches = 0
    for pred, label in zip(preds.tolist(), labels.tolist(), strict=True):
        if pred == label:
            matches += 1
    return matches / len(preds)


def best_threshold(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    """Scan sorted (score, label) pairs in a single Python loop to pick the best threshold."""
    if len(scores) == 0:
        return (0.0, 0.0)
    pairs = sorted(zip(scores.tolist(), labels.tolist(), strict=True), key=lambda pair: pair[0])
    total = len(pairs)
    right_ones = sum(1 for _, label in pairs if label == 1)
    left_zeros = 0

    best_t = float(pairs[0][0])
    best_acc = -1.0
    i = 0

    while i < total:
        t = pairs[i][0]
        acc = (left_zeros + right_ones) / total
        if acc > best_acc:
            best_acc = acc
            best_t = float(t)
        while i < total and pairs[i][0] == t:
            if pairs[i][1] == 1:
                right_ones -= 1
            else:
                left_zeros += 1
            i += 1

    return (float(best_t), round(float(best_acc), 3))
