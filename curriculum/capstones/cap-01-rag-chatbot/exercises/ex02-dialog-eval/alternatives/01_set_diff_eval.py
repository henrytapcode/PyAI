REFUSAL = "I don't know based on the provided context."


def _eval_single_dialog(make_bot, dialog: dict) -> list[dict]:
    """Evaluate one dialog on its own bot instance and return 1-indexed turn rows."""
    bot = make_bot()
    dialog_id = dialog["id"]
    rows: list[dict] = []
    for turn_idx, turn in enumerate(dialog["turns"], 1):
        reason = score_turn(bot.ask(turn["question"]), turn)
        rows.append(
            {
                "dialog": dialog_id,
                "turn": turn_idx,
                "ok": reason is None,
                "reason": reason,
            }
        )
    return rows


def score_turn(result: dict, turn: dict) -> str | None:
    """Score one turn by checking refusal rules, source match, and case-insensitive facts."""
    answer = result["answer"]
    sources = result["sources"]
    expected_source = turn["expected_source"]

    if expected_source is None:
        return None if (answer == REFUSAL and sources == []) else "no_refusal"

    checks = [
        (answer == REFUSAL, "refused"),
        (expected_source not in sources, "wrong_source"),
        (
            any(fact.lower() not in answer.lower() for fact in turn["expected_facts"]),
            "missing_fact",
        ),
    ]
    return next((label for failed, label in checks if failed), None)


def run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]:
    """Evaluate all dialogs in order, isolating each dialog behind its own ``make_bot()``."""
    return [row for dialog in dialogs for row in _eval_single_dialog(make_bot, dialog)]


def compare_to_baseline(
    current: list[dict],
    baseline: list[dict],
    min_pass_rate: float = 0.8,
) -> dict:
    """Compare runs using key-indexed dicts and set intersections ordered by ``current``."""
    if not current:
        raise ValueError("current must not be empty")

    order = [(item["dialog"], item["turn"]) for item in current]
    current_by_key = {(item["dialog"], item["turn"]): item for item in current}
    baseline_ok = {(item["dialog"], item["turn"]): bool(item["ok"]) for item in baseline}

    cur_pass = {key for key, item in current_by_key.items() if item["ok"]}
    cur_fail = set(current_by_key) - cur_pass
    base_pass = {key for key, ok in baseline_ok.items() if ok}
    base_fail = set(baseline_ok) - base_pass

    fixed_keys = cur_pass & base_fail
    broken_keys = cur_fail & base_pass
    new_keys = set(current_by_key) - set(baseline_ok)

    fixed = [key for key in order if key in fixed_keys]
    broken = [key for key in order if key in broken_keys]
    new = [key for key in order if key in new_keys]
    failures = [
        (key[0], key[1], current_by_key[key]["reason"])
        for key in order
        if key in cur_fail
    ]

    passed_count = sum(1 for item in current if item["ok"])
    pass_rate = round(passed_count / len(current), 3)
    gate_ok = not broken and pass_rate >= min_pass_rate
    return {
        "pass_rate": pass_rate,
        "fixed": fixed,
        "broken": broken,
        "new": new,
        "failures": failures,
        "gate_ok": gate_ok,
    }
