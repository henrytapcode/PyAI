"""Text-cleaning toolkit, part 1: the config and the text functions.

Complete the config and the three functions: write your code inside them and `return` the answer.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class CleanConfig:
    """Settings for clean_text.

    Example:
        CleanConfig() -> lowercase=True, drop_urls=True, max_chars=None
    """

    # TODO 1: add three fields with defaults:
    #   lowercase (bool, True), drop_urls (bool, True), max_chars (int or None, None)
    pass


def normalize_spaces(text: str) -> str:
    """Replace every run of spaces, tabs and newlines with one space and trim both ends.

    Example:
        normalize_spaces("  a   b \n") -> "a b"
    """
    # TODO 2: split the text into words, then join them with one space
    return None


def remove_urls(text: str) -> str:
    """Drop every word that starts with "http://" or "https://", joining the rest with one space.

    Example:
        remove_urls("see https://example.com now") -> "see now"
    """
    # TODO 3: keep only the words that do not start with those prefixes, then join
    return None


def clean_text(text: str, config: CleanConfig | None = None) -> str:
    """Clean one text. Raise TypeError("text must be a string") when it is not a string.

    Steps, in this order, each one only if the config says so:
    remove URLs, fix spaces (always), lowercase, cut to max_chars and strip the right end.

    Example:
        clean_text("  Read https://x.io  TODAY ") -> "read today"
    """
    # TODO 4: check the type and use CleanConfig() when config is None
    # TODO 5: apply the steps in order
    return None
