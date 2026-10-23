from exercise import CALL_LOG, record_calls


@record_calls
def add(a, b=0):
    """Add two numbers."""
    return a + b


@record_calls
def hello():
    return "hi"


def test_returns_what_the_function_returns():
    CALL_LOG.clear()
    assert add(2, 3) == 5, "the wrapper must return the result of the original function"


def test_works_with_keyword_arguments():
    CALL_LOG.clear()
    assert add(2, b=3) == 5, "pass **kwargs on to the original function"


def test_works_without_arguments():
    CALL_LOG.clear()
    assert hello() == "hi"


def test_records_the_name_and_the_positional_arguments():
    CALL_LOG.clear()
    add(2, 3)
    assert CALL_LOG == [("add", (2, 3))]


def test_keyword_arguments_are_not_part_of_the_recorded_tuple():
    CALL_LOG.clear()
    add(2, b=3)
    assert CALL_LOG == [("add", (2,))]


def test_every_call_is_recorded_in_order():
    CALL_LOG.clear()
    add(1, 1)
    hello()
    add(5)
    assert CALL_LOG == [("add", (1, 1)), ("hello", ()), ("add", (5,))]


def test_keeps_the_name_and_docstring():
    assert add.__name__ == "add", "put @wraps(func) above the wrapper"
    assert add.__doc__ == "Add two numbers."
