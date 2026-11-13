import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def train_and_score(X: np.ndarray, y: np.ndarray, seed: int) -> float:
    """Split X and y with stratify=y, fit a pipeline, and return rounded test accuracy.

    Example: on load_iris(return_X_y=True) with seed=42, returns 0.921.
    """
    X_train, X_test, y_train, y_test = ___(
        X, y, test_size=0.25, random_state=seed, stratify=y
    )
    pipe = make_pipeline(___(), LogisticRegression())
    pipe.___(X_train, y_train)
    return round(float(pipe.score(___, y_test)), 3)
