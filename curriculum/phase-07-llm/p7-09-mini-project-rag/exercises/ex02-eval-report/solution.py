def evaluate_bot(answer_fn, eval_set: list[dict]) -> dict:
    """Evaluate answer_fn on eval_set and classify retrieval, answer, and refusal failures."""
    hits = 0
    n_answerable = 0
    facts_ok = 0
    idk_ok = 0
    n_unanswerable = 0
    failures: list[tuple[str, str]] = []

    for row in eval_set:
        out = answer_fn(row["question"])
        ans_low = out["answer"].lower()
        expected_src = row["expected_source"]
        if expected_src is None:
            n_unanswerable += 1
            if "i don't know" in ans_low and not out["sources"]:
                idk_ok += 1
            else:
                failures.append((row["id"], "no_refusal"))
        else:
            n_answerable += 1
            hit = expected_src in out["retrieved"]
            facts = all(fact.lower() in ans_low for fact in row["expected_facts"])
            if hit:
                hits += 1
            if facts:
                facts_ok += 1
            if not hit:
                failures.append((row["id"], "retrieval_miss"))
            elif not facts:
                failures.append((row["id"], "answer_miss"))

    return {
        "n": len(eval_set),
        "hits": hits,
        "n_answerable": n_answerable,
        "facts_ok": facts_ok,
        "idk_ok": idk_ok,
        "n_unanswerable": n_unanswerable,
        "failures": failures,
    }


def report_lines(summary: dict) -> list[str]:
    """Format summary counts, percentages (or n/a), and failure lines."""

    def fmt(num: int, den: int) -> str:
        if den == 0:
            return "n/a"
        return f"{num}/{den} ({round(num / den * 100)}%)"

    lines = [
        f"hit@k: {fmt(summary['hits'], summary['n_answerable'])}",
        f"facts: {fmt(summary['facts_ok'], summary['n_answerable'])}",
        f"refusals: {fmt(summary['idk_ok'], summary['n_unanswerable'])}",
    ]
    for qid, reason in summary["failures"]:
        lines.append(f"FAIL {qid}: {reason}")
    lines.append(f"failures: {len(summary['failures'])}")
    return lines
