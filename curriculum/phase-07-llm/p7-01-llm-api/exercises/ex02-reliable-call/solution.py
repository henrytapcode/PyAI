from pyai_llm import FakeLLM, RateLimitError, Usage


def ask_with_retry(
    client: FakeLLM,
    messages: list[dict[str, str]],
    max_attempts: int = 3,
) -> tuple[str, int]:
    """Call client.chat(messages), retrying RateLimitError up to max_attempts times.

    Example: ask_with_retry(FakeLLM(fail_times=2), msgs, max_attempts=3) -> ("...", 3)
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.chat(messages)
            return resp.content or "", attempt
        except RateLimitError:
            if attempt == max_attempts:
                raise
    raise RuntimeError("unreachable")


def estimate_cost(
    usage: Usage,
    price_in_per_m: float,
    price_out_per_m: float,
) -> float:
    """Return USD cost for usage rounded to 6 decimal places.

    Example: estimate_cost(Usage(1000, 500, 1500), 0.50, 1.50) -> 0.00125
    """
    in_cost = (usage.prompt_tokens / 1_000_000) * price_in_per_m
    out_cost = (usage.completion_tokens / 1_000_000) * price_out_per_m
    return round(in_cost + out_cost, 6)
