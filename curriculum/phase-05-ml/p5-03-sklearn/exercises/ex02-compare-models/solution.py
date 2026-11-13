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
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )
    scores: dict[str, float] = {}
    for name, model in models.items():
        fitted = clone(model)
        fitted.fit(X_train, y_train)
        scores[name] = round(float(fitted.score(X_test, y_test)), 3)
    return scores


def best_model(scores: dict[str, float]) -> str:
    """Return the highest-scoring name (alphabetically on ties); raise ValueError if empty.

    Example: best_model({"zeta": 0.9, "alpha": 0.9, "beta": 0.8}) -> "alpha"
    """
    if not scores:
        raise ValueError("scores must not be empty")
    best_name = ""
    best_score = -1.0
    for name, score in scores.items():
        if score > best_score or (score == best_score and name < best_name):
            best_score = score
            best_name = name
    return best_name
