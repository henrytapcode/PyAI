import numpy as np
from sklearn.base import clone
from sklearn.model_selection import train_test_split


def _test_score(
    model,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> float:
    """Fit a clone on train and return its rounded test accuracy."""
    fitted = clone(model).fit(X_train, y_train)
    return round(float(fitted.score(X_test, y_test)), 3)


def compare_models(
    X: np.ndarray,
    y: np.ndarray,
    models: dict,
    seed: int,
) -> dict[str, float]:
    """Evaluate cloned models with a dict comprehension over one shared split."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )
    return {
        name: _test_score(model, X_train, X_test, y_train, y_test)
        for name, model in models.items()
    }


def best_model(scores: dict[str, float]) -> str:
    """Pick the highest score (alphabetically first on ties) using a tuple key."""
    if not scores:
        raise ValueError("scores must not be empty")
    name, _ = min(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    return name
