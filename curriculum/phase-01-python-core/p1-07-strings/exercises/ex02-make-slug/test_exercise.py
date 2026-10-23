import pytest

from exercise import make_slug


def test_simple_title():
    assert make_slug("Hello World") == "hello-world"


def test_uses_hyphens_not_underscores():
    assert "_" not in make_slug("a b c"), "words must be joined with a hyphen, not an underscore"


def test_lowercases_everything():
    assert make_slug("Python For AI") == "python-for-ai", "remember: lower() returns a new string"


def test_removes_spaces_at_both_ends():
    assert make_slug("  Hello World  ") == "hello-world"


def test_collapses_repeated_spaces():
    assert make_slug("a    b") == "a-b", "split() with nothing inside ignores extra spaces"


@pytest.mark.parametrize("title, slug", [
    ("Single", "single"),
    ("My First   RAG App", "my-first-rag-app"),
    ("   ", ""),
])
def test_other_titles(title, slug):
    assert make_slug(title) == slug
