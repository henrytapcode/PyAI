"""Alternative solution: filter valid plans and encode plan_code with NumPy boolean masks."""

import numpy as np
import pandas as pd

VALID_PLANS = ("free", "pro", "enterprise")


def prepare_features(raw: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Clean raw support ticket logs using boolean-mask encoding instead of Series.map."""
    df = raw.drop_duplicates(subset=["ticket_id"], keep="first").copy()
    df["plan"] = df["plan"].astype(str).str.strip().str.lower()
    df = df[df["plan"].isin(VALID_PLANS)]

    for col in ("tokens", "error_count", "hours_since_deploy"):
        series = (
            df[col].astype(str).str.replace(",", "", regex=False)
            if col == "tokens"
            else df[col]
        )
        df[col] = pd.to_numeric(series, errors="coerce")

    df = df.dropna(
        subset=["tokens", "error_count", "hours_since_deploy", "urgent"]
    ).reset_index(drop=True)
    plan_code = (
        (df["plan"] == "pro").to_numpy(dtype="float64")
        + 2.0 * (df["plan"] == "enterprise").to_numpy(dtype="float64")
    )
    X = np.column_stack([
        df["tokens"].to_numpy(dtype="float64"),
        df["error_count"].to_numpy(dtype="float64"),
        df["hours_since_deploy"].to_numpy(dtype="float64"),
        plan_code,
    ])
    y = df["urgent"].to_numpy(dtype="int64")
    return X, y
