import pytest

from exercise import retry


def make_flaky(fail_times, error=ValueError):
    """A stub that raises for its first `fail_times` calls, then returns twice its input."""
    calls = []

    def flaky(x):
        calls.append(x)
        if len(calls) <= fail_times:
            raise error(f"boom {len(calls)}")
        return x * 2

    return flaky, calls


def test_returns_the_result_when_the_first_call_works():
    flaky, calls = make_flaky(0)
    assert retry(3)(flaky)(5) == 10
    assert len(calls) == 1, "do not call the function again after it worked"


def test_tries_again_until_a_call_works():
    flaky, calls = make_flaky(2)
    assert retry(3)(flaky)(5) == 10
    assert len(calls) == 3


def test_works_with_the_at_syntax():
    flaky, calls = make_flaky(1)

    @retry(2)
    def ask(x):
        return flaky(x)

    assert ask(4) == 8
    assert len(calls) == 2


def test_gives_up_after_exactly_times_attempts():
    flaky, calls = make_flaky(10)
    with pytest.raises(ValueError):
        retry(3)(flaky)(1)
    assert len(calls) == 3, "stop after `times` attempts, the first try counts"


def test_raises_the_error_of_the_last_attempt():
    flaky, calls = make_flaky(10)
    with pytest.raises(ValueError) as info:
        retry(3)(flaky)(1)
    assert str(info.value) == "boom 3", "raise the error of the last attempt, not the first"


def test_one_attempt_means_no_retry():
    flaky, calls = make_flaky(10)
    with pytest.raises(ValueError):
        retry(1)(flaky)(1)
    assert len(calls) == 1


@pytest.mark.parametrize("error", [ValueError, TimeoutError, KeyError, RuntimeError])
def test_retries_any_kind_of_exception(error):
    flaky, calls = make_flaky(1, error)
    assert retry(2)(flaky)(3) == 6
    assert len(calls) == 2


def test_passes_positional_and_keyword_arguments():
    seen = []

    @retry(2)
    def join(a, b, sep="-"):
        seen.append((a, b, sep))
        return a + sep + b

    assert join("x", "y") == "x-y"
    assert join("x", b="y", sep="+") == "x+y"
    assert seen == [("x", "y", "-"), ("x", "y", "+")]


def test_keeps_the_name_and_docstring():
    @retry(2)
    def ask_llm(prompt):
        """Send a prompt."""
        return prompt

    assert ask_llm.__name__ == "ask_llm", "put @wraps(func) above the wrapper"
    assert ask_llm.__doc__ == "Send a prompt."


def test_each_decorated_function_counts_its_own_attempts():
    first, first_calls = make_flaky(1)
    second, second_calls = make_flaky(2)
    wrapped_first = retry(2)(first)
    wrapped_second = retry(3)(second)
    assert wrapped_first(1) == 2
    assert wrapped_second(1) == 2
    assert len(first_calls) == 2
    assert len(second_calls) == 3
