import numpy as np
from sklearn.base import clone
from sklearn.model_selection import train_test_split


def compare_models(
    X: np.ndarray,
    y: np.ndarray,
    models: dict,
    seed: int,
) -> dict[str, float]:
    """Evaluate cloned models on one stratified 70/30 split and return rounded test accuracies.

    Example (X, y from make_classification(
        n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
    )):
        pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
        compare_models(X, y, {"knn": pipe}, seed=42) -> {"knn": 0.833}
    """
    # TODO: split (X, y) once with test_size=0.3, random_state=seed, stratify=y
    # TODO: clone each model, fit on train, record round(float(score), 3) on test
    return {}


def best_model(scores: dict[str, float]) -> str:
    """Return the highest-scoring name (alphabetically on ties); raise ValueError if empty.

    Example: best_model({"zeta": 0.9, "alpha": 0.9, "beta": 0.8}) -> "alpha"
    """
    # TODO: raise ValueError if scores is empty
    # TODO: pick the highest score, breaking ties by alphabetical order
    return ""
