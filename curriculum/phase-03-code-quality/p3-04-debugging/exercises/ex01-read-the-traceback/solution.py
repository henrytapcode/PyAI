def parse_line(line: str) -> dict:
    """Turn one log line into a dict.

    Example:
        parse_line("model=small tokens=120 latency=0.84s")
        -> {"model": "small", "tokens": 120, "latency": 0.84}
    """
    parts = dict(item.split("=") for item in line.split())
    return {
        "model": parts["model"],
        "tokens": int(parts["tokens"]),
        "latency": float(parts["latency"].rstrip("s")),
    }


def summarize(lines: list[str]) -> tuple[int, float]:
    """Return (total_tokens, average_latency) for the log lines. Skip blank lines.

    Example:
        summarize(["model=a tokens=100 latency=1.0s", "", "model=a tokens=50 latency=2.0s"])
        -> (150, 1.5)
    """
    records = [parse_line(line) for line in lines if line.strip()]
    if not records:
        return 0, 0.0
    total_tokens = sum(r["tokens"] for r in records)
    average = sum(r["latency"] for r in records) / len(records)
    return total_tokens, average
