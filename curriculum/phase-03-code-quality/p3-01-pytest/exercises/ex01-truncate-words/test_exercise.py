import pytest

from exercise import truncate_words


def test_short_text_is_unchanged():
    assert truncate_words("hello world", 5) == "hello world"


def test_long_text_is_cut_and_marked():
    assert truncate_words("one two three four", 2) == "one two..."


def test_exact_limit_is_not_marked():
    assert truncate_words("one two three", 3) == "one two three"


def test_empty_text_gives_empty_text():
    assert truncate_words("", 3) == ""


def test_extra_spaces_are_collapsed():
    assert truncate_words("  one   two  ", 5) == "one two"


def test_zero_limit_cuts_everything():
    assert truncate_words("one two", 0) == "..."


def test_negative_limit_raises_value_error():
    with pytest.raises(ValueError):
        truncate_words("one two", -1)
