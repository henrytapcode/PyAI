"""A step logger written as a context manager.

Replace each ___ with the right word, then press Check.
"""
from contextlib import contextmanager


@contextmanager
def logged_step(log, name):
    """Add "start <name>" before the block and "end <name>" after it.

    Example: with logged_step(log, "embed") as step: ...
    leaves log == ["start embed", "end embed"], and step == "embed"
    """
    log.append("start " + name)
    try:
        yield name
    finally:
        log.append("end " + name)
