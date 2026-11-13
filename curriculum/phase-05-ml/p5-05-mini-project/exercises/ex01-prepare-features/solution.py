"""Mini-project part 1: clean raw ticket logs into (X, y) NumPy arrays."""

import numpy as np
import pandas as pd

PLAN_MAP = {"free": 0.0, "pro": 1.0, "enterprise": 2.0}
FEATURE_COLS = ["tokens", "error_count", "hours_since_deploy", "plan_code"]


def prepare_features(raw: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Clean raw support ticket logs and return (X, y) without target leakage.

    Example:
        raw = pd.DataFrame({
            "ticket_id": ["t01", "t01"],
            "plan": [" PRO", "free"],
            "tokens": ["1,200", "500"],
            "error_count": [2.0, 0.0],
            "hours_since_deploy": [4.5, 10.0],
            "escalated_to_oncall": [1, 0],
            "urgent": [1, 0],
        })
        X, y = prepare_features(raw)
        # X.shape == (1, 4), X[0].tolist() == [1200.0, 2.0, 4.5, 1.0], y.tolist() == [1]
    """
    df = raw.copy()
    df["plan"] = df["plan"].astype(str).str.strip().str.lower()
    df["tokens"] = pd.to_numeric(
        df["tokens"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )
    df["error_count"] = pd.to_numeric(df["error_count"], errors="coerce")
    df["hours_since_deploy"] = pd.to_numeric(df["hours_since_deploy"], errors="coerce")
    df = df.drop_duplicates(subset=["ticket_id"], keep="first")
    df["plan_code"] = df["plan"].map(PLAN_MAP)
    df = df.dropna(subset=[*FEATURE_COLS, "urgent"]).reset_index(drop=True)
    X = df[FEATURE_COLS].to_numpy(dtype="float64")
    y = df["urgent"].to_numpy(dtype="int64")
    return X, y
