import numpy as np


def split_data(
    X: np.ndarray,
    y: np.ndarray,
    test_ratio: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Shuffle rows with seed and return (X_train, X_test, y_train, y_test).

    Example: split_data(np.arange(10).reshape(5, 2), np.arange(5), 0.2, 42)
    returns arrays of lengths (4, 1, 4, 1).
    """
    rng = np.random.default_rng(___)
    idx = rng.___(len(X))
    n_test = int(round(len(X) * ___))
    test_idx = idx[:___]
    train_idx = idx[___:]
    return X[train_idx], X[___], y[train_idx], y[___]
