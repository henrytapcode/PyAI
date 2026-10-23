"""Load exam scores from text and log what happened."""
import logging

logger = logging.getLogger(__name__)


def load_scores(raw_scores):
    """Turn strings into ints, skip the bad ones, and log what happened.

    load_scores(["10", "abc", "7"]) -> [10, 7]
    It logs a WARNING "skipping bad score: abc", then an INFO "loaded 2 of 3 scores".
    """
    # TODO 1: start with an empty list for the good scores
    # TODO 2: loop over raw_scores and try to convert each text with int(...)
    # TODO 3: on ValueError, log a WARNING and go on with the next text
    # TODO 4: after the loop, log one INFO message with the counts
    return None
