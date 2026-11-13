import matplotlib.pyplot as plt
import pandas as pd
import pytest

from exercise import model_report, plot_report


def _clean_sample() -> pd.DataFrame:
    return pd.DataFrame({
        "request_id": ["r01", "r02", "r03", "r04", "r05", "r06", "r07"],
        "model": ["gpt-4o", "gpt-4o", "gpt-4o", "claude", "claude", "mini", "mini"],
        "tokens": pd.Series([1200, 900, 1100, 750, 650, 300, 250], dtype="int64"),
        "latency_ms": [850.0, 920.0, float("nan"), 620.0, 580.0, 210.0, 190.0],
        "status": ["ok", "ok", "error", "ok", "ok", "ok", "ok"],
        "rating": [5.0, 4.0, float("nan"), 5.0, 4.0, 4.0, 3.0],
    })


def test_report_columns_and_index():
    report = model_report(_clean_sample())
    assert list(report.columns) == [
        "model",
        "requests",
        "total_tokens",
        "error_rate",
        "avg_latency",
        "avg_rating",
    ]
    assert report.index.tolist() == [0, 1, 2]


def test_report_aggregates_requests_and_total_tokens():
    report = model_report(_clean_sample())
    assert report["model"].tolist() == ["gpt-4o", "claude", "mini"]
    assert report["requests"].tolist() == [3, 2, 2]
    assert report["total_tokens"].tolist() == [3200, 1400, 550]


def test_report_rounds_error_rate_latency_and_rating():
    df = pd.DataFrame({
        "request_id": ["r1", "r2", "r3"],
        "model": ["claude", "claude", "claude"],
        "tokens": pd.Series([100, 200, 300], dtype="int64"),
        "latency_ms": [100.0, 100.0, 200.0],
        "status": ["error", "ok", "ok"],
        "rating": [5.0, 4.0, 2.0],
    })
    report = model_report(df)
    row = report.iloc[0]
    assert float(row["error_rate"]) == pytest.approx(0.333)
    assert float(row["avg_latency"]) == pytest.approx(133.3)
    assert float(row["avg_rating"]) == pytest.approx(3.67)


def test_report_handles_model_with_only_error_requests():
    df = pd.DataFrame({
        "request_id": ["r1", "r2", "r3"],
        "model": ["alpha", "alpha", "mini"],
        "tokens": pd.Series([100, 150, 500], dtype="int64"),
        "latency_ms": [300.0, 400.0, 100.0],
        "status": ["error", "error", "ok"],
        "rating": [1.0, 2.0, 5.0],
    })
    report = model_report(df)
    alpha = report[report["model"] == "alpha"].iloc[0]
    assert float(alpha["error_rate"]) == pytest.approx(1.0)


def test_report_ignores_nan_and_returns_nan_when_all_ratings_missing():
    df = pd.DataFrame({
        "request_id": ["r1", "r2", "r3", "r4"],
        "model": ["gpt-4o", "gpt-4o", "mini", "mini"],
        "tokens": pd.Series([500, 500, 100, 100], dtype="int64"),
        "latency_ms": [800.0, float("nan"), 200.0, 300.0],
        "status": ["ok", "ok", "ok", "ok"],
        "rating": [float("nan"), float("nan"), 4.0, float("nan")],
    })
    report = model_report(df)
    gpt_row = report[report["model"] == "gpt-4o"].iloc[0]
    mini_row = report[report["model"] == "mini"].iloc[0]
    assert float(gpt_row["avg_latency"]) == pytest.approx(800.0)
    assert pd.isna(gpt_row["avg_rating"]), "when all ratings are NaN, avg_rating should be NaN"
    assert float(mini_row["avg_rating"]) == pytest.approx(4.0)


def test_report_breaks_total_token_ties_alphabetically():
    df = pd.DataFrame({
        "request_id": ["r1", "r2", "r3"],
        "model": ["zeta", "alpha", "beta"],
        "tokens": pd.Series([500, 500, 900], dtype="int64"),
        "latency_ms": [100.0, 100.0, 100.0],
        "status": ["ok", "ok", "ok"],
        "rating": [4.0, 4.0, 4.0],
    })
    report = model_report(df)
    assert report["model"].tolist() == ["beta", "alpha", "zeta"]


def test_report_does_not_modify_input_dataframe():
    df = _clean_sample()
    snapshot = df.to_dict("list")
    _ = model_report(df)
    assert list(df.columns) == list(snapshot.keys())
    assert len(df) == len(snapshot["request_id"])
    assert df["tokens"].tolist() == snapshot["tokens"]


def test_plot_report_bars_labels_and_titles_match_report():
    report = model_report(_clean_sample())
    fig, ax = plot_report(report)
    try:
        heights = [float(p.get_height()) for p in ax.patches]
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["gpt-4o", "claude", "mini"]
        assert heights == pytest.approx([3200.0, 1400.0, 550.0])
        assert ax.get_title() == "Tokens by model"
        assert ax.get_ylabel() == "tokens"
    finally:
        plt.close(fig)


def test_plot_report_does_not_modify_input_report():
    report = model_report(_clean_sample())
    expected_models = report["model"].tolist()
    expected_tokens = report["total_tokens"].tolist()
    fig, _ax = plot_report(report)
    try:
        assert report["model"].tolist() == expected_models
        assert report["total_tokens"].tolist() == expected_tokens
    finally:
        plt.close(fig)
