import pytest

from exercise import clean_prompts


def test_cleans_the_example_from_the_prompt():
    result = clean_prompts(["  Hello   WORLD ", "", "   ", "What IS AI?"])
    assert result == ["hello world", "what is ai?"]


def test_returns_a_list():
    assert isinstance(clean_prompts(["Hi"]), list), "return a list, not None"


def test_makes_text_lowercase():
    assert clean_prompts(["SUMMARIZE This"]) == ["summarize this"]


def test_strips_spaces_at_both_ends():
    assert clean_prompts(["   hello   "]) == ["hello"]


def test_squeezes_inner_whitespace_to_one_space():
    assert clean_prompts(["a   b\t\tc\nd"]) == ["a b c d"]


def test_drops_empty_and_blank_prompts():
    assert clean_prompts(["", "  ", "\t\n", "ok"]) == ["ok"]


def test_returns_empty_list_when_nothing_is_left():
    assert clean_prompts(["", "   "]) == []
    assert clean_prompts([]) == []


def test_keeps_order_and_duplicates():
    result = clean_prompts(["B", "a", "B", "A"])
    assert result == ["b", "a", "b", "a"]


def test_does_not_change_the_input_list():
    original = ["  Hi  ", "", "THERE"]
    copy = list(original)
    result = clean_prompts(original)
    assert original == copy, "do not modify the list that was passed in"
    assert result is not original


@pytest.mark.parametrize("prompt, expected", [
        ("Hello", "hello"),
        (" What  is   RAG? ", "what is rag?"),
        ("ONE", "one"),
    ])
def test_single_prompt_cases(prompt, expected):
    assert clean_prompts([prompt]) == [expected]
