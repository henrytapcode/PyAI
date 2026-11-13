import pandas as pd


def average_score_by_model(df: pd.DataFrame) -> dict[str, float]:
    """Return {model: rounded mean score} for rows where status == "ok"."""
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for row in df.itertuples(index=False):
        if row.status != "ok":
            continue
        model = str(row.model)
        totals[model] = totals.get(model, 0.0) + float(row.score)
        counts[model] = counts.get(model, 0) + 1
    return {model: round(totals[model] / counts[model], 2) for model in totals}
