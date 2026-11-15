from pyai_llm import FakeLLM, RateLimitError, Usage


def ask_with_retry(
    client: FakeLLM,
    messages: list[dict[str, str]],
    max_attempts: int = 3,
) -> tuple[str, int]:
    """Call client.chat(messages), retrying RateLimitError up to max_attempts times.

    Example: ask_with_retry(FakeLLM(fail_times=2), msgs, max_attempts=3) -> ("...", 3)
    """
    # TODO: retry RateLimitError up to max_attempts times and return (content, attempt)
    return None


def estimate_cost(
    usage: Usage,
    price_in_per_m: float,
    price_out_per_m: float,
) -> float:
    """Return USD cost for usage rounded to 6 decimal places.

    Example: estimate_cost(Usage(1000, 500, 1500), 0.50, 1.50) -> 0.00125
    """
    # TODO: compute input + output cost from per-1M-token prices and round to 6 decimals
    return None
