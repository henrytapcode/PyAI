import pytest
from exercise import ask_with_retry, estimate_cost
from pyai_llm import FakeLLM, RateLimitError, Usage


class _BadRequestSpy:
    def __init__(self) -> None:
        self.calls = 0

    def chat(self, messages: list[dict[str, str]]) -> object:
        self.calls += 1
        raise ValueError("invalid role")


def test_succeeds_on_first_attempt():
    client = FakeLLM()
    result = ask_with_retry(client, [{"role": "user", "content": "What is RAG?"}])
    assert result is not None, (
        "ask_with_retry returned None: did you forget to return (content, attempts)?"
    )
    content, attempts = result
    assert attempts == 1
    assert "RAG" in content


def test_succeeds_after_transient_rate_limits():
    client = FakeLLM(fail_times=2)
    result = ask_with_retry(
        client,
        [{"role": "user", "content": "What is temperature?"}],
        max_attempts=3,
    )
    assert result is not None, (
        "ask_with_retry returned None: did you forget to return (content, attempts)?"
    )
    content, attempts = result
    assert attempts == 3
    assert "Temperature" in content


def test_raises_rate_limit_when_attempts_exhausted():
    client = FakeLLM(fail_times=3)
    with pytest.raises(RateLimitError):
        ask_with_retry(
            client,
            [{"role": "user", "content": "What is RAG?"}],
            max_attempts=3,
        )


def test_does_not_retry_value_error():
    spy = _BadRequestSpy()
    with pytest.raises(ValueError):
        ask_with_retry(spy, [{"role": "bot", "content": "Hi"}], max_attempts=3)
    assert spy.calls == 1, "ValueError is not transient and must not be retried"


def test_ask_with_retry_return_types():
    client = FakeLLM()
    result = ask_with_retry(client, [{"role": "user", "content": "What is a token?"}])
    assert result is not None, (
        "ask_with_retry returned None: did you forget to return (content, attempts)?"
    )
    assert isinstance(result, tuple) and len(result) == 2
    content, attempts = result
    assert isinstance(content, str)
    assert type(attempts) is int


def test_estimate_cost_known_values():
    usage = Usage(prompt_tokens=1000, completion_tokens=500, total_tokens=1500)
    cost = estimate_cost(usage, price_in_per_m=0.50, price_out_per_m=1.50)
    assert cost is not None, (
        "estimate_cost returned None: did you forget to return the rounded float?"
    )
    assert type(cost) is float
    assert cost == pytest.approx(0.00125)


def test_estimate_cost_rounds_to_six_decimals():
    usage = Usage(prompt_tokens=139, completion_tokens=57, total_tokens=196)
    cost = estimate_cost(usage, price_in_per_m=0.50, price_out_per_m=1.50)
    assert cost is not None, (
        "estimate_cost returned None: did you forget to return the rounded float?"
    )
    assert cost == 0.000155


def test_estimate_cost_rounds_beyond_six_decimals():
    usage = Usage(prompt_tokens=333, completion_tokens=777, total_tokens=1110)
    cost = estimate_cost(usage, price_in_per_m=0.35, price_out_per_m=1.25)
    assert cost is not None, (
        "estimate_cost returned None: did you forget to return the rounded float?"
    )
    assert cost == 0.001088, "round the final cost to 6 decimal places"
