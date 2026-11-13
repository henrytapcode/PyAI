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
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n_test = int(round(len(X) * test_ratio))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
