def evaluate_bot(answer_fn, eval_set: list[dict]) -> dict:
    """Evaluate answer_fn on eval_set and classify retrieval, answer, and refusal failures.

    Example:
        evaluate_bot(bot_fn, eval_set)
        -> {"n": 2, "hits": 1, "n_answerable": 1, "facts_ok": 1,
            "idk_ok": 1, "n_unanswerable": 1, "failures": []}
    """
    # TODO: iterate eval_set without mutating it, score hits/facts/idk,
    # and record (id, reason) failures in eval_set order.
    return None


def report_lines(summary: dict) -> list[str]:
    """Format summary counts, percentages (or n/a), and failure lines.

    Example:
        report_lines(summary)
        -> ["hit@k: 1/1 (100%)", "facts: 1/1 (100%)", "refusals: 1/1 (100%)", "failures: 0"]
    """
    # TODO: format hit@k, facts, refusals, FAIL lines, and total failures count.
    return None
