import logging

logger = logging.getLogger("app.llm")


def check_reply(reply: str, attempt: int, max_attempts: int = 3) -> bool:
    """Return True when the model reply has text. Log what happened at the right level.

    Example:
        check_reply("hello", 1) -> True  (and logs a DEBUG record)
    """
    if reply:
        logger.debug("reply has %d characters", len(reply))
        return True
    if attempt < max_attempts:
        logger.warning("empty reply, retrying (attempt %d)", attempt)
        return False
    logger.error("giving up after %d attempts", attempt)
    return False
