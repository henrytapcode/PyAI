from pyai_llm import FakeLLM, RateLimitError, Usage


def ask_with_retry(
    client: FakeLLM,
    messages: list[dict[str, str]],
    max_attempts: int = 3,
) -> tuple[str, int]:
    """Call client.chat(messages) using a while loop to retry RateLimitError."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    attempt = 1
    while attempt <= max_attempts:
        try:
            resp = client.chat(messages)
            return resp.content or "", attempt
        except RateLimitError:
            if attempt == max_attempts:
                raise
            attempt += 1
    raise RuntimeError("unreachable")


def estimate_cost(
    usage: Usage,
    price_in_per_m: float,
    price_out_per_m: float,
) -> float:
    """Return USD cost for usage rounded to 6 decimal places."""
    total_dollars = (
        usage.prompt_tokens * price_in_per_m + usage.completion_tokens * price_out_per_m
    ) / 1_000_000
    return round(total_dollars, 6)
