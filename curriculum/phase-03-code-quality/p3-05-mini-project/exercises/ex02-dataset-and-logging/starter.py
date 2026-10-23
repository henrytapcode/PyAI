"""Text-cleaning toolkit, part 2: clean a whole dataset and log what happened.

`CleanConfig`, `clean_text` and `CleanReport` are finished for you (part 1 and section 5).
Complete `clean_dataset`: write your code inside it and `return` the report.
"""
import logging
from dataclasses import dataclass

logger = logging.getLogger("textclean")


@dataclass(frozen=True)
class CleanConfig:
    lowercase: bool = True
    drop_urls: bool = True
    max_chars: int | None = None


def clean_text(text: str, config: CleanConfig | None = None) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if config is None:
        config = CleanConfig()
    words = text.split()
    if config.drop_urls:
        words = [w for w in words if not w.startswith(("http://", "https://"))]
    text = " ".join(words)
    if config.lowercase:
        text = text.lower()
    if config.max_chars is not None:
        text = text[: config.max_chars].rstrip()
    return text


@dataclass
class CleanReport:
    kept: list[str]
    skipped: int = 0
    empty: int = 0
    duplicates: int = 0


def clean_dataset(texts: list, config: CleanConfig | None = None) -> CleanReport:
    """Clean every item of `texts` and return a CleanReport. Log what happened.

    Example:
        clean_dataset(["Hi  there", "hi there", "", 7])
        -> CleanReport(kept=["hi there"], skipped=1, empty=1, duplicates=1)
        and logs WARNING "skipping item 3: not a string"
        and logs INFO "kept 1 of 4 texts"
    """
    # TODO 1: start with CleanReport(kept=[]) and an empty set of texts already seen
    # TODO 2: loop with enumerate; a non-string item: log a WARNING and count it in skipped
    # TODO 3: clean the string; empty -> count in empty; seen before -> count in duplicates;
    #         otherwise remember it and keep it
    # TODO 4: log one INFO line "kept %d of %d texts" and return the report
    return None
