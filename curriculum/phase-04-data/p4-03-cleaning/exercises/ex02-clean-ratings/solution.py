import pandas as pd


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean user names and numeric ratings (1-5), keeping the last row per user."""
    out = df.copy()
    out["user"] = out["user"].str.strip().str.lower()
    out["rating"] = pd.to_numeric(out["rating"], errors="coerce")
    out = out.dropna(subset=["rating"])
    out = out[out["rating"].between(1, 5) & (out["rating"] % 1 == 0)]
    out = out.drop_duplicates(subset=["user"], keep="last")
    out["rating"] = out["rating"].astype("int64")
    return out[["user", "rating"]].reset_index(drop=True)
