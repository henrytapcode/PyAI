import pandas as pd


def average_score_by_model(df: pd.DataFrame) -> dict[str, float]:
    """Return {model: rounded mean score} for rows where status == "ok".

    Example: average_score_by_model(df) -> {"gpt-4o": 0.93, "llama": 0.8}
    """
    ok_rows = df[df["status"] == "ok"]
    means = ok_rows.groupby("model")["score"].mean()
    return {str(model): round(float(score), 2) for model, score in means.items()}
