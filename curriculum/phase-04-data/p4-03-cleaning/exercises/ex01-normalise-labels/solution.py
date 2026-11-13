import pandas as pd


def normalise_labels(labels: pd.Series) -> pd.Series:
    """Clean label text: strip outer whitespace, lowercase, replace _ and - with spaces.

    Example: normalise_labels(pd.Series([" Bug_Report ", "FEATURE-REQ"]))
    -> Series(["bug report", "feature req"])
    """
    cleaned = labels.str.strip().str.lower()
    cleaned = cleaned.str.replace("_", " ", regex=False)
    return cleaned.str.replace("-", " ", regex=False)
