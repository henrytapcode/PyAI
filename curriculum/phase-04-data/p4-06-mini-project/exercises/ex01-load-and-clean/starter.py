"""Mini-project part 1: load and clean raw chatbot API log CSV text."""
import io
import pandas as pd


def load_and_clean(csv_text: str) -> pd.DataFrame:
    """Load raw CSV logs and return a cleaned 6-column DataFrame.

    Example:
        csv = 'request_id,model,tokens,latency_ms,status,rating\nr01, GPT-4o,"1,200",850,ok,5'
        load_and_clean(csv) -> 1-row DataFrame with model="gpt-4o" and tokens=1200 (int64)
    """
    # TODO 1: read csv_text with pd.read_csv(io.StringIO(csv_text))
    # TODO 2: normalise "model" (strip, lower, "_" -> "-")
    # TODO 3: strip commas from "tokens" and coerce "tokens", "latency_ms", "rating" to numeric
    # TODO 4: mask "rating" outside 1..5 to NaN
    # TODO 5: drop duplicate "request_id" (keep="first") and rows missing "tokens"
    # TODO 6: reset index (drop=True), cast "tokens" to "int64", return the 6 columns in order
    return None
