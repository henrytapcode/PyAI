import io
import pandas as pd

COLUMNS = ["request_id", "model", "tokens", "latency_ms", "status", "rating"]


def load_and_clean(csv_text: str) -> pd.DataFrame:
    """Load raw CSV logs and return a cleaned 6-column DataFrame."""
    df = pd.read_csv(io.StringIO(csv_text))
    df["model"] = (
        df["model"].astype(str).str.strip().str.lower().str.replace("_", "-", regex=False)
    )
    clean_tokens = df["tokens"].astype(str).str.replace(",", "", regex=False)
    df["tokens"] = pd.to_numeric(clean_tokens, errors="coerce")
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce").astype("float64")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("float64")
    df["rating"] = df["rating"].where(df["rating"].between(1, 5))
    df = df.drop_duplicates(subset=["request_id"], keep="first")
    df = df.dropna(subset=["tokens"]).reset_index(drop=True)
    df["tokens"] = df["tokens"].astype("int64")
    return df[COLUMNS]
