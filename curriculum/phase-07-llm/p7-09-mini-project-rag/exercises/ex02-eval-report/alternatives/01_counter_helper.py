from collections import Counter


def _classify_case(row: dict, out: dict) -> tuple[bool, list[str], str | None]:
    ans_low = out["answer"].lower()
    expected_src = row["expected_source"]
    if expected_src is None:
        ok = "i don't know" in ans_low and len(out["sources"]) == 0
        return False, (["idk_ok"] if ok else []), (None if ok else "no_refusal")

    hit = expected_src in out["retrieved"]
    facts = all(fact.lower() in ans_low for fact in row["expected_facts"])
    keys: list[str] = []
    if hit:
        keys.append("hits")
    if facts:
        keys.append("facts_ok")
    if not hit:
        reason: str | None = "retrieval_miss"
    elif not facts:
        reason = "answer_miss"
    else:
        reason = None
    return True, keys, reason


def evaluate_bot(answer_fn, eval_set: list[dict]) -> dict:
    """Evaluate answer_fn by delegating per-row classification and tallying with Counter."""
    counts: Counter[str] = Counter()
    failures: list[tuple[str, str]] = []

    for row in eval_set:
        is_ans, keys, reason = _classify_case(row, answer_fn(row["question"]))
        counts["n_answerable" if is_ans else "n_unanswerable"] += 1
        counts.update(keys)
        if reason is not None:
            failures.append((row["id"], reason))

    return {
        "n": len(eval_set),
        "hits": counts["hits"],
        "n_answerable": counts["n_answerable"],
        "facts_ok": counts["facts_ok"],
        "idk_ok": counts["idk_ok"],
        "n_unanswerable": counts["n_unanswerable"],
        "failures": failures,
    }


def report_lines(summary: dict) -> list[str]:
    """Format summary counts, percentages (or n/a), and failure lines."""
    rows = [
        ("hit@k", summary["hits"], summary["n_answerable"]),
        ("facts", summary["facts_ok"], summary["n_answerable"]),
        ("refusals", summary["idk_ok"], summary["n_unanswerable"]),
    ]
    lines = [
        f"{label}: {'n/a' if den == 0 else f'{num}/{den} ({round(num / den * 100)}%)'}"
        for label, num, den in rows
    ]
    lines.extend(f"FAIL {qid}: {reason}" for qid, reason in summary["failures"])
    lines.append(f"failures: {len(summary['failures'])}")
    return lines
