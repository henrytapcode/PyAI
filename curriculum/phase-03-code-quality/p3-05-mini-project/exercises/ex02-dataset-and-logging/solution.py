"""Text-cleaning toolkit, part 2: clean a whole dataset and log what happened."""
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
    report = CleanReport(kept=[])
    seen = set()
    for index, item in enumerate(texts):
        if not isinstance(item, str):
            logger.warning("skipping item %d: not a string", index)
            report.skipped += 1
            continue
        cleaned = clean_text(item, config)
        if not cleaned:
            report.empty += 1
        elif cleaned in seen:
            report.duplicates += 1
        else:
            seen.add(cleaned)
            report.kept.append(cleaned)
    logger.info("kept %d of %d texts", len(report.kept), len(texts))
    return report
