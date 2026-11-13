import matplotlib.pyplot as plt
import pandas as pd


def model_report(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned logs by model using pure pandas groupby().agg()."""
    work = df.copy()
    work["is_error"] = (work["status"] == "error").astype("float64")
    report = work.groupby("model", as_index=False).agg(
        requests=("request_id", "count"),
        total_tokens=("tokens", "sum"),
        error_rate=("is_error", "mean"),
        avg_latency=("latency_ms", "mean"),
        avg_rating=("rating", "mean"),
    )
    report["error_rate"] = report["error_rate"].round(3)
    report["avg_latency"] = report["avg_latency"].round(1)
    report["avg_rating"] = report["avg_rating"].round(2)
    report = report.sort_values(
        by=["total_tokens", "model"],
        ascending=[False, True],
    ).reset_index(drop=True)
    return report


def plot_report(report: pd.DataFrame) -> tuple:
    """Draw a bar chart of total_tokens by model and return (fig, ax)."""
    fig, ax = plt.subplots()
    ax.bar(report["model"].tolist(), report["total_tokens"].tolist())
    ax.set_title("Tokens by model")
    ax.set_ylabel("tokens")
    return fig, ax
