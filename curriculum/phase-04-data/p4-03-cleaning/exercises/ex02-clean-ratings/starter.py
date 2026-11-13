import pandas as pd


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean user names and numeric ratings (1-5), keeping the last row per user.

    Example: clean_ratings(pd.DataFrame({"user": [" An ", "an"], "rating": [" 4 ", "5"]}))
    -> DataFrame({"user": ["an"], "rating": [5]})
    """
    # TODO: copy df, normalise "user" (strip + lower)
    # TODO: coerce "rating" to numeric, drop NaN and values outside 1..5
    # TODO: keep only the last row per user, cast "rating" to int64, reset index
    return df
