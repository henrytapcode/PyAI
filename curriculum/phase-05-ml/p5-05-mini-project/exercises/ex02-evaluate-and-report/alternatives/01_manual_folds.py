"""Alternative solution: run CV folds manually with StratifiedKFold.split and clone."""

import numpy as np
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def evaluate_models(X: np.ndarray, y: np.ndarray, seed: int) -> dict[str, tuple[float, float]]:
    """Run manual 5-fold stratified CV using clone() and f1_score(..., zero_division=0)."""
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    models = [
        ("baseline", DummyClassifier(strategy="most_frequent")),
        ("logreg", make_pipeline(StandardScaler(), LogisticRegression())),
        ("tree", DecisionTreeClassifier(max_depth=3, random_state=0)),
    ]
    results: dict[str, tuple[float, float]] = {}
    for name, template in models:
        fold_scores: list[float] = []
        for train_idx, val_idx in skf.split(X, y):
            model = clone(template)
            model.fit(X[train_idx], y[train_idx])
            preds = model.predict(X[val_idx])
            fold_scores.append(float(f1_score(y[val_idx], preds, zero_division=0)))
        arr = np.array(fold_scores, dtype="float64")
        results[name] = (round(float(arr.mean()), 3), round(float(arr.std()), 3))
    return results


def write_report(results: dict[str, tuple[float, float]], n_test: int) -> list[str]:
    """Format CV results into honest report lines without mutating results."""
    non_baseline = [(name, stats) for name, stats in results.items() if name != "baseline"]
    if not non_baseline:
        raise ValueError("results must include at least one non-baseline model")

    ranked = sorted(non_baseline, key=lambda item: (-item[1][0], item[0]))
    lines = [f"{name} F1: {mean:.3f} +/- {std:.3f}" for name, (mean, std) in results.items()]
    lines.extend([f"best: {ranked[0][0]}", f"test size: {n_test}"])

    if len(ranked) >= 2:
        (name_a, (mean_a, std_a)), (name_b, (mean_b, std_b)) = ranked[0], ranked[1]
        if abs(mean_a - mean_b) < max(std_a, std_b):
            lines.append(f"warning: {name_a} and {name_b} differ by less than one std")

    return lines
