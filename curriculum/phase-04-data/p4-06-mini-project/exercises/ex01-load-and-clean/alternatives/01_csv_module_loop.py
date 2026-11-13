import csv
import io
import pandas as pd

COLUMNS = ["request_id", "model", "tokens", "latency_ms", "status", "rating"]


def _parse_float(value: str | None) -> float:
    if value is None or not value.strip():
        return float("nan")
    try:
        return float(value)
    except ValueError:
        return float("nan")


def load_and_clean(csv_text: str) -> pd.DataFrame:
    """Clean raw request log CSV text row by row with csv.DictReader."""
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    seen_ids: set[str] = set()
    rows: list[dict] = []

    for raw in reader:
        req_id = raw["request_id"]
        if req_id in seen_ids:
            continue
        seen_ids.add(req_id)

        token_text = (raw.get("tokens") or "").replace(",", "").strip()
        if not token_text:
            continue
        try:
            tokens = int(float(token_text))
        except ValueError:
            continue

        model = (raw.get("model") or "").strip().lower().replace("_", "-")
        latency = _parse_float(raw.get("latency_ms"))
        rating = _parse_float(raw.get("rating"))
        if not (1.0 <= rating <= 5.0):
            rating = float("nan")

        rows.append({
            "request_id": req_id,
            "model": model,
            "tokens": tokens,
            "latency_ms": latency,
            "status": raw["status"],
            "rating": rating,
        })

    df = pd.DataFrame(rows, columns=COLUMNS)
    df["tokens"] = df["tokens"].astype("int64")
    df["latency_ms"] = df["latency_ms"].astype("float64")
    df["rating"] = df["rating"].astype("float64")
    return df
