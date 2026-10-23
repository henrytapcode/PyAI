import logging

logger = logging.getLogger("app.llm")


def check_reply(reply: str, attempt: int, max_attempts: int = 3) -> bool:
    """Return True when the model reply has text. Log what happened at the right level.

    Example:
        check_reply("hello", 1) -> True  (and logs a DEBUG record)
    """
    # Replace each ___ with a logging method name: debug, info, warning, error or critical.
    if reply:
        logger.___("reply has %d characters", len(reply))  # a detail for bug hunting
        return True
    if attempt < max_attempts:
        logger.___("empty reply, retrying (attempt %d)", attempt)  # odd, but we carry on
        return False
    logger.___("giving up after %d attempts", attempt)  # the operation failed
    return False
