"""Mini-project part 2: 5-fold stratified CV evaluation and honest reporting."""

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def evaluate_models(X: np.ndarray, y: np.ndarray, seed: int) -> dict[str, tuple[float, float]]:
    """Run 5-fold stratified CV for baseline, logreg, and tree; return {name: (mean, std)}."""
    # TODO 1: create StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    # TODO 2: create make_scorer(f1_score, zero_division=0)
    # TODO 3: evaluate "baseline", "logreg", and "tree" and store rounded Python (mean, std) floats
    return None


def write_report(results: dict[str, tuple[float, float]], n_test: int) -> list[str]:
    """Format CV results into honest report lines, flagging close top models.

    Example:
        results = {"baseline": (0.0, 0.0), "logreg": (0.709, 0.092), "tree": (0.701, 0.14)}
        write_report(results, 58)
        # ['baseline F1: 0.000 +/- 0.000', 'logreg F1: 0.709 +/- 0.092',
        #  'tree F1: 0.701 +/- 0.140', 'best: logreg', 'test size: 58',
        #  'warning: logreg and tree differ by less than one std']
    """
    # TODO 1: collect non-baseline entries; raise ValueError if none exist
    # TODO 2: format "<name> F1: <mean:.3f> +/- <std:.3f>" for each entry in results
    # TODO 3: append "best: <name>" and "test size: <n_test>"
    # TODO 4: if top two non-baseline models differ by < max(std_a, std_b), append warning line
    return None
