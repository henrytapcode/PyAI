import numpy as np


def cosine_sim(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two numeric lists, rounded to 3 decimals.

    Example: cosine_sim([3.0, 4.0], [6.0, 8.0]) -> 1.0
    """
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    norm_a = float(np.linalg.norm(va))
    norm_b = float(np.linalg.norm(vb))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    score = (va @ vb) / (norm_a * norm_b)
    return round(float(score), 3)
