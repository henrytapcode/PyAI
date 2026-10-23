# Clean a small dataset, count what is dropped, and log one warning per bad item plus a summary.
import logging
import sys
from dataclasses import dataclass

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s %(name)s %(message)s",
    force=True,
)
logger = logging.getLogger("textclean")


def clean_text(text):
    words = [w for w in text.split() if not w.startswith(("http://", "https://"))]
    return " ".join(words).lower()


@dataclass
class CleanReport:
    kept: list[str]
    skipped: int = 0
    empty: int = 0
    duplicates: int = 0


def clean_dataset(texts):
    report = CleanReport(kept=[])
    seen = set()
    for index, item in enumerate(texts):
        if not isinstance(item, str):
            logger.warning("skipping item %d: not a string", index)
            report.skipped += 1
            continue
        cleaned = clean_text(item)
        if not cleaned:
            report.empty += 1
        elif cleaned in seen:
            report.duplicates += 1
        else:
            seen.add(cleaned)
            report.kept.append(cleaned)
    logger.info("kept %d of %d texts", len(report.kept), len(texts))
    return report


raw = [
    "How to reset a password",
    "how to RESET a password https://help.io/a",
    "https://only.a/link",
    None,
    "What is an embedding?",
    "",
    404,
]
report = clean_dataset(raw)
print(report.kept)
print(report.skipped, report.empty, report.duplicates)
