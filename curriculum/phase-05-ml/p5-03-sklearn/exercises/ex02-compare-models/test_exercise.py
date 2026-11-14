import pytest
from sklearn.datasets import make_classification
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from exercise import best_model, compare_models


def test_compare_models_returns_expected_scores_and_order():
    X, y = make_classification(
        n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
    )
    models = {
        "logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "knn": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3)),
        "tree": DecisionTreeClassifier(max_depth=3, random_state=0),
    }
    scores = compare_models(X, y, models, seed=42)
    assert list(scores.keys()) == ["logreg", "knn", "tree"]
    assert all(type(v) is float for v in scores.values()), "every score must be a Python float"
    assert scores == {"logreg": 0.722, "knn": 0.833, "tree": 0.722}


def test_identical_models_get_identical_scores():
    X, y = make_classification(
        n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
    )
    models = {
        "first": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "second": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    }
    scores = compare_models(X, y, models, seed=7)
    assert scores["first"] == scores["second"], (
        "identical models must get identical scores on the shared split"
    )


def test_caller_models_remain_unfitted():
    X, y = make_classification(
        n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
    )
    logreg = LogisticRegression(max_iter=1000)
    pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
    compare_models(X, y, {"logreg": logreg, "pipe": pipe}, seed=42)
    with pytest.raises(NotFittedError):
        logreg.predict(X[:2])
    with pytest.raises(NotFittedError):
        pipe.predict(X[:2])


def test_best_model_picks_highest_score():
    assert best_model({"logreg": 0.722, "knn": 0.833, "tree": 0.75}) == "knn"


def test_best_model_breaks_ties_alphabetically():
    assert best_model({"zeta": 0.9, "alpha": 0.9, "beta": 0.8}) == "alpha"


def test_best_model_raises_on_empty_dict():
    with pytest.raises(ValueError):
        best_model({})
