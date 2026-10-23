import typing

from exercise import average_length, find_system, repeat, shout


def hints(function):
    # helper: reads the hints the way a type checker would
    # get_type_hints turns the stored hints into real types, even if they were saved as text
    return typing.get_type_hints(function)


def test_average_length_of_words():
    assert average_length(["ab", "abcd"]) == 3.0
    assert average_length(["abc"]) == 3.0


def test_average_length_of_empty_list_is_zero():
    assert average_length([]) == 0.0


def test_average_length_hint_says_float():
    hint = hints(average_length)["return"]
    assert hint is float, "/ always gives a float, so the hint should say float"


def test_average_length_still_takes_a_list_of_str():
    assert hints(average_length)["words"] == list[str]


def test_find_system_returns_the_first_system_text():
    messages = [
        {"role": "user", "text": "Hi"},
        {"role": "system", "text": "Be brief."},
        {"role": "system", "text": "Second"},
    ]
    assert find_system(messages) == "Be brief."


def test_find_system_returns_none_when_missing():
    assert find_system([{"role": "user", "text": "Hi"}]) is None
    assert find_system([]) is None


def test_find_system_hint_allows_none():
    hint = hints(find_system)["return"]
    members = set(typing.get_args(hint))
    assert members == {str, type(None)}, "it can return None, so the hint must be str | None"


def test_repeat_repeats_the_word():
    assert repeat("ab", 2) == "abab"
    assert repeat("x", 0) == ""


def test_repeat_hint_says_word_is_str():
    assert hints(repeat)["word"] is str, "you repeat text, so word is a str"
    assert hints(repeat)["times"] is int
    assert hints(repeat)["return"] is str


def test_shout_returns_the_capital_letters():
    assert shout("hi") == "HI", "shout must return the result, not just compute it"
    assert shout("Hello there") == "HELLO THERE"


def test_shout_hint_stays_str():
    assert hints(shout)["text"] is str
    assert hints(shout)["return"] is str
