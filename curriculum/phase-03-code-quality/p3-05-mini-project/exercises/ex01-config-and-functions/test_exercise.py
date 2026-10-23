import pytest

from exercise import CleanConfig, clean_text, normalize_spaces, remove_urls


def test_config_defaults():
    config = CleanConfig()
    assert config.lowercase is True
    assert config.drop_urls is True
    assert config.max_chars is None


def test_config_options_can_be_set_by_name():
    config = CleanConfig(lowercase=False, max_chars=5)
    assert config.lowercase is False
    assert config.drop_urls is True
    assert config.max_chars == 5


def test_config_is_frozen():
    config = CleanConfig()
    with pytest.raises(AttributeError):
        config.lowercase = False


@pytest.mark.parametrize(
    "text, expected",
    [
        ("  a   b ", "a b"),
        ("a\n\tb", "a b"),
        ("one", "one"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_normalize_spaces(text, expected):
    assert normalize_spaces(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("see https://example.com now", "see now"),
        ("http://a.io and https://b.io", "and"),
        ("no links here", "no links here"),
        ("https://only.url", ""),
        ("www.example.com stays", "www.example.com stays"),
    ],
)
def test_remove_urls(text, expected):
    assert remove_urls(text) == expected


def test_clean_text_with_the_default_config():
    assert clean_text("  Hello   World  ") == "hello world"
    assert clean_text("Read https://x.io today") == "read today"


def test_clean_text_can_keep_capital_letters():
    config = CleanConfig(lowercase=False)
    assert clean_text("Hello  WORLD", config) == "Hello WORLD"


def test_clean_text_can_keep_urls():
    config = CleanConfig(drop_urls=False)
    assert clean_text("see   https://x.io", config) == "see https://x.io"


@pytest.mark.parametrize(
    "max_chars, expected",
    [
        (11, "hello brave"),
        (6, "hello"),
        (100, "hello brave new world"),
        (0, ""),
    ],
)
def test_clean_text_cuts_to_max_chars(max_chars, expected):
    config = CleanConfig(max_chars=max_chars)
    assert clean_text("hello brave new world", config) == expected, "cut last, then strip"


@pytest.mark.parametrize("bad", [5, None, ["a"]])
def test_clean_text_rejects_a_non_string(bad):
    with pytest.raises(TypeError):
        clean_text(bad)
