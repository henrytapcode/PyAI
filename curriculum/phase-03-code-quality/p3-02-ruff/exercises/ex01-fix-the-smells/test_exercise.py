import pytest

from exercise import collect, parse_count, total_length


def test_collect_returns_the_item_in_a_list():
    assert collect("a") == ["a"]


def test_collect_gives_a_fresh_list_on_every_call():
    assert collect("a") == ["a"]
    assert collect("b") == ["b"], "the default list is shared between calls (B006)"


def test_collect_adds_to_the_list_you_pass_in():
    mine = ["x"]
    result = collect("y", mine)
    assert result == ["x", "y"]
    assert result is mine


def test_parse_count_reads_a_number():
    assert parse_count("12") == 12


def test_parse_count_returns_minus_one_for_text():
    assert parse_count("abc") == -1


def test_parse_count_does_not_hide_other_errors():
    with pytest.raises(TypeError):
        parse_count(None)


def test_total_length_adds_every_text():
    assert total_length(["ab", "c"]) == 3, "the loop must add to `total` (F841 shows the typo)"


def test_total_length_of_nothing_is_zero():
    assert total_length([]) == 0
