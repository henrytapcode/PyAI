import pytest

from exercise import TokenCounter


def test_new_counter_starts_at_zero():
    counter = TokenCounter()
    assert counter.total == 0, "a new counter needs self.total = 0 in __init__"
    assert counter.calls == 0, "a new counter needs self.calls = 0 in __init__"


def test_add_increases_total():
    counter = TokenCounter()
    counter.add(10)
    counter.add(20)
    assert counter.total == 30, "add(n) must add n to self.total every time"


def test_add_counts_the_calls():
    counter = TokenCounter()
    counter.add(10)
    counter.add(20)
    counter.add(5)
    assert counter.calls == 3, "add(n) must also add 1 to self.calls"


def test_add_returns_nothing():
    counter = TokenCounter()
    assert counter.add(7) is None


def test_average_of_two_calls():
    counter = TokenCounter()
    counter.add(10)
    counter.add(20)
    assert counter.average() == pytest.approx(15.0)


def test_average_is_not_whole_number_division():
    counter = TokenCounter()
    counter.add(1)
    counter.add(2)
    assert counter.average() == pytest.approx(1.5)


def test_average_is_zero_when_nothing_was_added():
    counter = TokenCounter()
    assert counter.average() == 0, "with no calls, return 0 instead of dividing by zero"


def test_each_counter_keeps_its_own_numbers():
    chat = TokenCounter()
    search = TokenCounter()
    chat.add(50)
    search.add(7)
    chat.add(1)
    assert (chat.total, chat.calls) == (51, 2)
    assert (search.total, search.calls) == (7, 1)


def test_print_shows_total_and_calls(capsys):
    counter = TokenCounter()
    counter.add(10)
    counter.add(20)
    print(counter)
    assert capsys.readouterr().out == "TokenCounter(total=30, calls=2)\n"


def test_print_of_new_counter(capsys):
    print(TokenCounter())
    assert capsys.readouterr().out == "TokenCounter(total=0, calls=0)\n"


def test_repr_returns_text_and_does_not_print(capsys):
    counter = TokenCounter()
    counter.add(4)
    text = repr(counter)
    assert text == "TokenCounter(total=4, calls=1)", "__repr__ must return the text"
    assert capsys.readouterr().out == "", "__repr__ must return the text, not print it"
