"""Load exam scores from text and log what happened."""
import logging

logger = logging.getLogger(__name__)


def load_scores(raw_scores):
    """Turn strings into ints, skip the bad ones, and log what happened.

    load_scores(["10", "abc", "7"]) -> [10, 7]
    It logs a WARNING "skipping bad score: abc", then an INFO "loaded 2 of 3 scores".
    """
    scores = []
    for text in raw_scores:
        try:
            scores.append(int(text))
        except ValueError:
            logger.warning("skipping bad score: %s", text)
    logger.info("loaded %d of %d scores", len(scores), len(raw_scores))
    return scores
