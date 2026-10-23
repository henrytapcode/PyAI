"""Load exam scores with f-strings and a counter of skipped texts."""
import logging

logger = logging.getLogger(__name__)


def load_scores(raw_scores):
    scores = []
    skipped = 0
    for text in raw_scores:
        try:
            scores.append(int(text))
        except ValueError:
            skipped += 1
            logger.warning(f"skipping bad score: {text}")
    good = len(raw_scores) - skipped
    logger.info(f"loaded {good} of {len(raw_scores)} scores")
    return scores
