# Clean messy product reviews with two different configs.
from dataclasses import dataclass


@dataclass(frozen=True)
class CleanConfig:
    lowercase: bool = True
    drop_urls: bool = True
    max_chars: int | None = None


def normalize_spaces(text):
    return " ".join(text.split())


def remove_urls(text):
    words = [w for w in text.split() if not w.startswith(("http://", "https://"))]
    return " ".join(words)


def clean_text(text, config=None):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if config is None:
        config = CleanConfig()
    if config.drop_urls:
        text = remove_urls(text)
    text = normalize_spaces(text)
    if config.lowercase:
        text = text.lower()
    if config.max_chars is not None:
        text = text[: config.max_chars].rstrip()
    return text


reviews = [
    "  Great   PRODUCT!! see https://shop.io/r/1  ",
    "Too SLOW   to answer http://x.io",
    "ok",
]
normal = CleanConfig()
short = CleanConfig(lowercase=False, max_chars=12)

for review in reviews:
    print(repr(clean_text(review, normal)), "|", repr(clean_text(review, short)))
