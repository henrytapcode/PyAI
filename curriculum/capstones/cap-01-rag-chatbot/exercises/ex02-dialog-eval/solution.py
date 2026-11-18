REFUSAL = "I don't know based on the provided context."


def score_turn(result: dict, turn: dict) -> str | None:
    """Return None if ``result`` satisfies ``turn``, else the first failure reason."""
    answer = result["answer"]
    sources = result["sources"]
    expected_source = turn["expected_source"]

    if expected_source is None:
        if answer == REFUSAL and sources == []:
            return None
        return "no_refusal"

    if answer == REFUSAL:
        return "refused"
    if expected_source not in sources:
        return "wrong_source"

    lowered_answer = answer.lower()
    for fact in turn["expected_facts"]:
        if fact.lower() not in lowered_answer:
            return "missing_fact"
    return None


def run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]:
    """Run each dialog against a fresh ``make_bot()`` instance and score every turn."""
    records: list[dict] = []
    for dialog in dialogs:
        bot = make_bot()
        dialog_id = dialog["id"]
        for turn_num, turn in enumerate(dialog["turns"], 1):
            reply = bot.ask(turn["question"])
            reason = score_turn(reply, turn)
            records.append(
                {
                    "dialog": dialog_id,
                    "turn": turn_num,
                    "ok": reason is None,
                    "reason": reason,
                }
            )
    return records


def compare_to_baseline(
    current: list[dict],
    baseline: list[dict],
    min_pass_rate: float = 0.8,
) -> dict:
    """Diff ``current`` turn results against ``baseline`` and enforce the regression gate."""
    if not current:
        raise ValueError("current must not be empty")

    baseline_status: dict[tuple[str, int], bool] = {}
    for item in baseline:
        baseline_status[(item["dialog"], item["turn"])] = bool(item["ok"])

    fixed: list[tuple[str, int]] = []
    broken: list[tuple[str, int]] = []
    new: list[tuple[str, int]] = []
    failures: list[tuple[str, int, str | None]] = []
    passed_count = 0

    for item in current:
        key = (item["dialog"], item["turn"])
        is_ok = bool(item["ok"])
        if is_ok:
            passed_count += 1
        else:
            failures.append((item["dialog"], item["turn"], item["reason"]))

        if key not in baseline_status:
            new.append(key)
        elif is_ok and not baseline_status[key]:
            fixed.append(key)
        elif not is_ok and baseline_status[key]:
            broken.append(key)

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
