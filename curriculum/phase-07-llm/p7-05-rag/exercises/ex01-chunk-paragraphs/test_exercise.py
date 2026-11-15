import pytest
from exercise import chunk_paragraphs


def test_merges_short_paragraphs_within_budget():
    text = "One two.\n\nThree.\n\nFour five six.\n\nSeven."
    assert chunk_paragraphs(text, max_words=3) == [
        "One two.\n\nThree.",
        "Four five six.",
        "Seven.",
    ]


def test_exact_boundary_word_count_merges_into_same_chunk():
    text = "Alpha beta.\n\nGamma delta.\n\nEpsilon."
    assert chunk_paragraphs(text, max_words=4) == [
        "Alpha beta.\n\nGamma delta.",
        "Epsilon.",
    ]


def test_oversized_paragraph_stays_intact_as_single_chunk():
    text = "Short intro.\n\nThis paragraph has six distinct words.\n\nEnding."
    assert chunk_paragraphs(text, max_words=3) == [
        "Short intro.",
        "This paragraph has six distinct words.",
        "Ending.",
    ]


def test_strips_whitespace_and_ignores_blank_paragraphs():
    text = "\n\n  First line.  \n\n   \t  \n\n  Second line. \n\n"
    assert chunk_paragraphs(text, max_words=5) == ["First line.\n\nSecond line."]


def test_empty_or_whitespace_returns_empty_list():
    assert chunk_paragraphs("", max_words=3) == []
    assert chunk_paragraphs("   \n\n  \t  ", max_words=3) == []


@pytest.mark.parametrize("bad_max", [0, -1, -10])
def test_non_positive_max_words_raises_value_error(bad_max):
    with pytest.raises(ValueError):
        chunk_paragraphs("Hello world.", max_words=bad_max)
