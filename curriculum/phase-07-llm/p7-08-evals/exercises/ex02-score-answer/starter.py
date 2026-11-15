import re


def score_grounded(answer: str, expected_facts: list[str], context: str) -> dict:
    """Score expected facts, content faithfulness, and source citations for an answer.

    Example:
        score_grounded("Refunds take 30 days. [1]", ["30 days"], "[1] Refunds take 30 days.")
        -> {"facts": 1.0, "faithful": True, "unsupported": [],
            "citations": [1], "bad_citations": []}
    """
    # TODO: compute lowercase fact coverage (and handle empty expected_facts via "i don't know")
    # TODO: extract unique [n] citations in order and compare against [n] line prefixes in context
    # TODO: tokenize content words (strip [n], regex [a-z0-9]+, len >= 4) and find unsupported words
    pass
