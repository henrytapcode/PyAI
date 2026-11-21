"""Text-cleaning toolkit, part 2: clean a whole dataset and log what happened."""
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("textclean")


@dataclass(frozen=True)
class CleanConfig:
    lowercase: bool = True
    drop_urls: bool = field(default=True)
    max_chars: int | None = field(default=None)


def clean_text(text: str, config: CleanConfig | None = None) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cfg = config if config is not None else CleanConfig()
    tokens = text.split()
    if cfg.drop_urls:
        tokens = [tok for tok in tokens if not tok.startswith(("http://", "https://"))]
    result = " ".join(tokens)
    if cfg.lowercase:
        result = result.lower()
    if cfg.max_chars is not None:
        return result[: cfg.max_chars].rstrip()
    return result


@dataclass
class CleanReport:
    kept: list[str]
    skipped: int = field(default=0)
    empty: int = field(default=0)
    duplicates: int = field(default=0)


def clean_dataset(texts: list, config: CleanConfig | None = None) -> CleanReport:
    """Clean every item of `texts` and return a CleanReport. Log what happened.

    Example:
        clean_dataset(["Hi  there", "hi there", "", 7])
        -> CleanReport(kept=["hi there"], skipped=1, empty=1, duplicates=1)
        and logs WARNING "skipping item 3: not a string"
        and logs INFO "kept 1 of 4 texts"
    """
    kept: list[str] = []
    seen: set[str] = set()
    skipped = 0
    empty = 0
    duplicates = 0

    for idx, raw in enumerate(texts):
        if not isinstance(raw, str):
            logger.warning("skipping item %d: not a string", idx)
            skipped += 1
            continue
        cleaned = clean_text(raw, config)
        if not cleaned:
            empty += 1
        elif cleaned in seen:
            duplicates += 1
        else:
            seen.add(cleaned)
            kept.append(cleaned)

    logger.info("kept %d of %d texts", len(kept), len(texts))
    return CleanReport(kept=kept, skipped=skipped, empty=empty, duplicates=duplicates)
