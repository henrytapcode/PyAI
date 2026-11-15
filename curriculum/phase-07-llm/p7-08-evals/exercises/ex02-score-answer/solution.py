import re


def _content_words(text: str) -> list[str]:
    cleaned = re.sub(r"\[\d+\]", "", text.lower())
    return [w for w in re.findall(r"[a-z0-9]+", cleaned) if len(w) >= 4]


def _extract_citations(answer: str, context: str) -> tuple[list[int], list[int]]:
    citations: list[int] = []
    for raw in re.findall(r"\[(\d+)\]", answer):
        num = int(raw)
        if num not in citations:
            citations.append(num)
    valid_sources = {int(raw) for raw in re.findall(r"^\s*\[(\d+)\]", context, flags=re.MULTILINE)}
    bad_citations = [num for num in citations if num not in valid_sources]
    return citations, bad_citations


def score_grounded(answer: str, expected_facts: list[str], context: str) -> dict:
    """Score expected facts, content faithfulness, and source citations for an answer.

    Example:
        score_grounded("Refunds take 30 days. [1]", ["30 days"], "[1] Refunds take 30 days.")
        -> {"facts": 1.0, "faithful": True, "unsupported": [],
            "citations": [1], "bad_citations": []}
    """
    ans_low = answer.lower()
    if not expected_facts:
        facts = 1.0 if "i don't know" in ans_low else 0.0
    else:
        matched = 0
        for fact in expected_facts:
            if fact.lower() in ans_low:
                matched += 1
        facts = matched / len(expected_facts)

    citations, bad_citations = _extract_citations(answer, context)
    if "i don't know" in ans_low:
        return {
            "facts": facts,
            "faithful": True,
            "unsupported": [],
            "citations": citations,
            "bad_citations": bad_citations,
        }

    ctx_words = set(_content_words(context))
    unsupported: list[str] = []
    for word in _content_words(answer):
        if word not in ctx_words and word not in unsupported:
            unsupported.append(word)

    faithful = len(unsupported) == 0 and len(citations) > 0 and len(bad_citations) == 0
    return {
        "facts": facts,
        "faithful": faithful,
        "unsupported": unsupported,
        "citations": citations,
        "bad_citations": bad_citations,
    }
