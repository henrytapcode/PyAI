import pandas as pd


def normalise_labels(labels: pd.Series) -> pd.Series:
    """Clean label text: strip outer whitespace, lowercase, replace _ and - with spaces.

    Example: normalise_labels(pd.Series([" Bug_Report ", "FEATURE-REQ"]))
    -> Series(["bug report", "feature req"])
    """
    cleaned = labels.___.strip().str.___()
    cleaned = cleaned.str.___("_", " ", regex=False)
    return cleaned.str.replace(___, " ", regex=False)
