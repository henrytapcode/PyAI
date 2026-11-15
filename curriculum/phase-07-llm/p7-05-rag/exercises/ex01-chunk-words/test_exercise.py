import pytest
from exercise import chunk_words


def test_basic_sliding_window():
    result = chunk_words("a b c d e", size=3, overlap=1)
    assert result == ["a b c", "c d e"]


def test_no_overlap():
    result = chunk_words("one two three four five", size=2, overlap=0)
    assert result == ["one two", "three four", "five"]


@pytest.mark.parametrize(
    ("text", "size", "overlap", "expected"),
    [
        ("a b c d", 4, 2, ["a b c d"]),
        ("a b c d e f", 4, 2, ["a b c d", "c d e f"]),
        ("w0 w1 w2 w3 w4 w5 w6 w7 w8 w9", 4, 1, ["w0 w1 w2 w3", "w3 w4 w5 w6", "w6 w7 w8 w9"]),
    ],
)
def test_overlap_avoids_redundant_trailing_window(text, size, overlap, expected):
    assert chunk_words(text, size, overlap) == expected


def test_text_shorter_than_size_returns_single_chunk():
    assert chunk_words("  hello   world  ", size=5, overlap=2) == ["hello world"]


def test_empty_or_whitespace_text_returns_empty_list():
    assert chunk_words("", size=3, overlap=1) == []
    assert chunk_words("   \n\t ", size=3, overlap=1) == []


@pytest.mark.parametrize(
    ("size", "overlap"),
    [
        (0, 0),
        (-2, 0),
        (3, -1),
        (3, 3),
        (3, 5),
    ],
)
def test_invalid_parameters_raise_value_error(size, overlap):
    with pytest.raises(ValueError):
        chunk_words("a b c d", size, overlap)
