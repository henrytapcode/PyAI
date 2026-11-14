import numpy as np
import pytest

from exercise import evaluate_models, write_report


@pytest.fixture
def synthetic_data() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(10)
    X = rng.normal(size=(120, 4))
    logits = 1.8 * X[:, 0] - 1.1 * X[:, 1] - 1.6
    y = (rng.random(120) < 1 / (1 + np.exp(-logits))).astype("int64")
    return X, y


def test_evaluate_models_returns_expected_keys_and_float_tuples(synthetic_data):
    X, y = synthetic_data
    results = evaluate_models(X, y, seed=0)
    assert list(results.keys()) == ["baseline", "logreg", "tree"]
    for stats in results.values():
        assert isinstance(stats, tuple) and len(stats) == 2
        assert type(stats[0]) is float and type(stats[1]) is float


def test_evaluate_models_matches_exact_cv_scores(synthetic_data):
    X, y = synthetic_data
    results = evaluate_models(X, y, seed=0)
    assert results["baseline"] == (0.0, 0.0)
    assert results["logreg"] == (0.66, 0.096)
    assert results["tree"] == (0.605, 0.215)


def test_evaluate_models_changes_with_seed_and_beats_baseline(synthetic_data):
    X, y = synthetic_data
    res = evaluate_models(X, y, seed=3)
    assert res["baseline"] == (0.0, 0.0)
    assert res["logreg"][0] > 0.5
    assert res["tree"][0] > 0.5


def test_evaluate_models_does_not_modify_inputs(synthetic_data):
    X, y = synthetic_data
    X_copy = X.copy()
    y_copy = y.copy()
    evaluate_models(X, y, seed=0)
    assert np.array_equal(X, X_copy)
    assert np.array_equal(y, y_copy)


def test_write_report_formats_lines_with_warning_when_close():
    results = {"baseline": (0.0, 0.0), "logreg": (0.709, 0.092), "tree": (0.701, 0.14)}
    lines = write_report(results, n_test=58)
    assert lines == [
        "baseline F1: 0.000 +/- 0.000",
        "logreg F1: 0.709 +/- 0.092",
        "tree F1: 0.701 +/- 0.140",
        "best: logreg",
        "test size: 58",
        "warning: logreg and tree differ by less than one std",
    ]


def test_write_report_omits_warning_when_gap_is_at_or_above_max_std():
    # Gap is 0.200; max std is 0.100 -> clearly separated, no warning
    clear = {"baseline": (0.0, 0.0), "logreg": (0.80, 0.10), "tree": (0.60, 0.08)}
    assert write_report(clear, n_test=40) == [
        "baseline F1: 0.000 +/- 0.000",
        "logreg F1: 0.800 +/- 0.100",
        "tree F1: 0.600 +/- 0.080",
        "best: logreg",
        "test size: 40",
    ]
    # Boundary: exact equality (0.75 - 0.5 == 0.25) is NOT strictly less than max std
    boundary = {"logreg": (0.75, 0.25), "tree": (0.5, 0.125)}
    assert write_report(boundary, n_test=40)[-1] == "test size: 40"


def test_write_report_breaks_ties_alphabetically():
    tied = {"baseline": (0.0, 0.0), "tree": (0.72, 0.05), "logreg": (0.72, 0.06)}
    lines = write_report(tied, n_test=50)
    assert "best: logreg" in lines
    assert lines[-1] == "warning: logreg and tree differ by less than one std"


def test_write_report_handles_single_non_baseline_model_without_mutating():
    results = {"baseline": (0.0, 0.0), "logreg": (0.68, 0.07)}
    snapshot = dict(results)
    lines = write_report(results, n_test=30)
    assert results == snapshot
    assert lines == [
        "baseline F1: 0.000 +/- 0.000",
        "logreg F1: 0.680 +/- 0.070",
        "best: logreg",
        "test size: 30",
    ]


@pytest.mark.parametrize("bad_results", [{}, {"baseline": (0.0, 0.0)}])
def test_write_report_raises_value_error_without_non_baseline_models(bad_results):
    with pytest.raises(ValueError):
        write_report(bad_results, n_test=58)
