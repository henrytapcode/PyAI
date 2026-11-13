import math

import pandas as pd


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean ratings row by row using a dict keyed by normalised user name."""
    latest: dict[str, int] = {}
    for raw_user, raw_rating in zip(df["user"], df["rating"]):  # noqa: B905
        if raw_user is None or raw_rating is None or isinstance(raw_rating, bool):
            continue
        text_rating = str(raw_rating).strip()
        if not text_rating:
            continue
        try:
            value = float(text_rating)
        except ValueError:
            continue
        if not math.isfinite(value) or value % 1 != 0 or not (1 <= value <= 5):
            continue
        user = str(raw_user).strip().lower()
        latest.pop(user, None)
        latest[user] = int(value)

    return pd.DataFrame({
        "user": pd.Series(list(latest.keys()), dtype="object"),
        "rating": pd.Series(list(latest.values()), dtype="int64"),
    })
