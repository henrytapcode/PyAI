import pandas as pd


def slow_requests(df: pd.DataFrame, limit_ms: int) -> pd.DataFrame:
    """Return slow requests (> limit_ms), sorted descending, with reset index.

    Example: slow_requests(df, 200) returns rows with latency_ms > 200.
    """
    slow = df.loc[df["latency_ms"] >= limit_ms, ["endpoint", "latency_ms"]]
    return slow.sort_values("latency_ms")
