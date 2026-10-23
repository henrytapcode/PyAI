"""Load exam scores with a small helper that returns None for a bad text."""
import logging

logger = logging.getLogger(__name__)


def parse_score(text):
    try:
        return int(text)
    except ValueError:
        logger.warning("skipping bad score: %s", text)
        return None


def load_scores(raw_scores):
    scores = []
    for text in raw_scores:
        score = parse_score(text)
        if score is not None:
            scores.append(score)
    logger.info("loaded %d of %d scores", len(scores), len(raw_scores))
    return scores
