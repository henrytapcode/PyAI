"""Mini-project part 1: clean raw ticket logs into (X, y) NumPy arrays."""

import numpy as np
import pandas as pd


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
    # TODO 1: copy raw so the input DataFrame is not modified
    # TODO 2: normalise "plan" (strip, lower) and strip commas from "tokens"
    # TODO 3: coerce "tokens", "error_count", and "hours_since_deploy" to numeric
    # TODO 4: drop duplicate "ticket_id" rows (keep="first")
    # TODO 5: map "plan" to 0.0/1.0/2.0 and drop rows missing features or "urgent"
    # TODO 6: return X (float64, 4 columns, no leakage) and y ("int64")
    return None
