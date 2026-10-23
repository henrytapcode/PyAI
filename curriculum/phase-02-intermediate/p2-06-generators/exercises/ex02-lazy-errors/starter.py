"""Lazy helpers for reading a log file.

Replace each ___ with the right word, then press Check.
"""


def error_lines(lines):
    """Yield every line that contains "ERROR", with spaces and the new line removed.

    Example: list(error_lines(["ok", "ERROR disk full"])) gives ["ERROR disk full"]
    """
    for line in ___:
        if "ERROR" in line:
            yield line.___()


def count_errors(lines):
    """Return how many lines contain "ERROR".

    Example: count_errors(["ERROR a", "ok", "ERROR b"]) returns 2
    """
    return ___(1 for line in error_lines(lines))
