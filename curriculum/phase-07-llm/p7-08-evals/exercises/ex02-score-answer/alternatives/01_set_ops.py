import re


def score_grounded(answer: str, expected_facts: list[str], context: str) -> dict:
    """Score facts, faithfulness, and citations using set operations and dict.fromkeys."""
    token_re = re.compile(r"[a-z0-9]+")
    cite_re = re.compile(r"\[(\d+)\]")
    ctx_cite_re = re.compile(r"^\s*\[(\d+)\]", flags=re.MULTILINE)

    ans_low = answer.lower()
    if not expected_facts:
        facts = 1.0 if "i don't know" in ans_low else 0.0
    else:
        facts = sum(1 for f in expected_facts if f.lower() in ans_low) / len(expected_facts)

    citations = list(dict.fromkeys(int(n) for n in cite_re.findall(answer)))
    valid_sources = {int(n) for n in ctx_cite_re.findall(context)}
    bad_citations = [n for n in citations if n not in valid_sources]

    if "i don't know" in ans_low:
        return {
            "facts": facts,
            "faithful": True,
            "unsupported": [],
            "citations": citations,
            "bad_citations": bad_citations,
        }

    ans_words = [w for w in token_re.findall(cite_re.sub("", ans_low)) if len(w) >= 4]
    ctx_set = {w for w in token_re.findall(cite_re.sub("", context.lower())) if len(w) >= 4}
    missing = set(ans_words) - ctx_set
    unsupported = [w for w in dict.fromkeys(ans_words) if w in missing]

    faithful = not unsupported and bool(citations) and not bad_citations
    return {
        "facts": facts,
        "faithful": faithful,
        "unsupported": unsupported,
        "citations": citations,
        "bad_citations": bad_citations,
    }
