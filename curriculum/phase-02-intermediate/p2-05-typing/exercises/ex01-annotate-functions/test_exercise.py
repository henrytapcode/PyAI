import typing

from exercise import build_prompt, count_tokens, first_and_count, word_lengths


def hint_of(function, name):
    # helper: reads the hints the way a type checker would
    # get_type_hints turns the stored hints into real types, even if they were saved as text
    return typing.get_type_hints(function).get(name)


def shape(hint):
    return typing.get_origin(hint), typing.get_args(hint)


def is_str_or_none(hint):
    return set(typing.get_args(hint)) == {str, type(None)}


def test_count_tokens_counts_the_items():
    assert count_tokens(["Hello", "world"]) == 2
    assert count_tokens([]) == 0


def test_count_tokens_takes_a_list_of_str():
    hint = hint_of(count_tokens, "tokens")
    assert shape(hint) == (list, (str,)), "tokens is a list of text: list[str]"


def test_count_tokens_returns_int():
    assert hint_of(count_tokens, "return") is int


def test_build_prompt_without_system_returns_the_question():
    assert build_prompt("Hi") == "Hi"


def test_build_prompt_puts_system_before_the_question():
    assert build_prompt("Hi", "Be brief.") == "Be brief.\nHi"


def test_build_prompt_system_hint_allows_str_and_none():
    hint = hint_of(build_prompt, "system")
    assert is_str_or_none(hint), "system may be a str or None: str | None"


def test_build_prompt_returns_str():
    assert hint_of(build_prompt, "return") is str


def test_build_prompt_keeps_the_question_hint_and_default():
    assert hint_of(build_prompt, "question") is str
    assert build_prompt.__defaults__ == (None,), "keep the default value None"


def test_word_lengths_maps_words_to_lengths():
    assert word_lengths(["hi", "hello"]) == {"hi": 2, "hello": 5}


def test_word_lengths_returns_dict_of_str_to_int():
    hint = hint_of(word_lengths, "return")
    assert shape(hint) == (dict, (str, int)), (
        "keys are words (str) and values are lengths (int): dict[str, int]"
    )


def test_first_and_count_returns_a_pair():
    assert first_and_count(["a", "b", "c"]) == ("a", 3)


def test_first_and_count_returns_tuple_of_str_and_int():
    hint = hint_of(first_and_count, "return")
    assert shape(hint) == (tuple, (str, int)), (
        "a fixed pair, first a str then an int: tuple[str, int]"
    )
