from dataclasses import dataclass


@dataclass(frozen=True)
class CleanConfig:
    lowercase: bool = True
    drop_urls: bool = True
    max_chars: int | None = None


def normalize_spaces(text: str) -> str:
    return " ".join(text.split())


def remove_urls(text: str) -> str:
    kept = []
    for word in text.split():
        if not word.startswith(("http://", "https://")):
            kept.append(word)
    return " ".join(kept)


def clean_text(text: str, config: CleanConfig | None = None) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    config = config or CleanConfig()
    steps = []
    if config.drop_urls:
        steps.append(remove_urls)
    steps.append(normalize_spaces)
    if config.lowercase:
        steps.append(str.lower)
    if config.max_chars is not None:
        limit = config.max_chars
        steps.append(lambda value: value[:limit].rstrip())
    for step in steps:
        text = step(text)
    return text
