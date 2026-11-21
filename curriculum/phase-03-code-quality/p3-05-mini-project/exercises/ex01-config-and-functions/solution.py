"""Text-cleaning toolkit, part 1: the config and the text functions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CleanConfig:
    """Settings for clean_text.

    Example:
        CleanConfig() -> lowercase=True, drop_urls=True, max_chars=None
    """

    lowercase: bool = True
    drop_urls: bool = True
    max_chars: int | None = None


def normalize_spaces(text: str) -> str:
    """Replace every run of spaces, tabs and newlines with one space and trim both ends.

    Example:
        normalize_spaces("  a   b \n") -> "a b"
    """
    return " ".join(text.split())


def remove_urls(text: str) -> str:
    """Drop every word that starts with "http://" or "https://", joining the rest with one space.

    Example:
        remove_urls("see https://example.com now") -> "see now"
    """
    words = [w for w in text.split() if not w.startswith(("http://", "https://"))]
    return " ".join(words)


def clean_text(text: str, config: CleanConfig | None = None) -> str:
    """Clean one text. Raise TypeError("text must be a string") when it is not a string.

    Steps, in this order, each one only if the config says so:
    remove URLs, fix spaces (always), lowercase, cut to max_chars and strip the right end.

    Example:
        clean_text("  Read https://x.io  TODAY ") -> "read today"
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cfg = config if config is not None else CleanConfig()
    cleaned = remove_urls(text) if cfg.drop_urls else text
    cleaned = normalize_spaces(cleaned)
    if cfg.lowercase:
        cleaned = cleaned.lower()
    if cfg.max_chars is not None:
        return cleaned[: cfg.max_chars].rstrip()
    return cleaned
