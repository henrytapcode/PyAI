import pandas as pd


def average_score_by_model(df: pd.DataFrame) -> dict[str, float]:
    """Return {model: rounded mean score} for rows where status == "ok".

    Example: average_score_by_model(df) -> {"gpt-4o": 0.93, "llama": 0.8}
    """
    # TODO: filter rows with status == "ok"
    # TODO: group by "model", take mean of "score", round to 2 decimals
    # TODO: return a plain Python dict with float values
    return {}
