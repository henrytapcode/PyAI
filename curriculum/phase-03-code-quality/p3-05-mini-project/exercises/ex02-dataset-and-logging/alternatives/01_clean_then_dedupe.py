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
    report = CleanReport(kept=[])
    cleaned_texts = []
    for index, item in enumerate(texts):
        if not isinstance(item, str):
            logger.warning("skipping item %d: not a string", index)
            report.skipped += 1
            continue
        cleaned = clean_text(item, config)
        if cleaned:
            cleaned_texts.append(cleaned)
        else:
            report.empty += 1
    report.kept = list(dict.fromkeys(cleaned_texts))
    report.duplicates = len(cleaned_texts) - len(report.kept)
    logger.info("kept %d of %d texts", len(report.kept), len(texts))
    return report
