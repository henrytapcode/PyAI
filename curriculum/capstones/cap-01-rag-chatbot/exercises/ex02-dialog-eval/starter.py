REFUSAL = "I don't know based on the provided context."


def score_turn(result: dict, turn: dict) -> str | None:
    """Return None if ``result`` satisfies ``turn``, else the first failure reason.

    Example:
        score_turn(
            {"answer": REFUSAL, "sources": []},
            {"question": "Crypto?", "expected_source": None, "expected_facts": []},
        )
        # -> None
    """
    # TODO:
    # 1. If turn["expected_source"] is None: pass only when answer == REFUSAL and sources == [];
    #    otherwise return "no_refusal".
    # 2. Otherwise check in priority order:
    #    - answer == REFUSAL -> "refused"
    #    - turn["expected_source"] not in sources -> "wrong_source"
    #    - any fact in turn["expected_facts"] missing from answer (case-insensitive)
    #      -> "missing_fact"
    # 3. Return None when all checks pass.
    return None


def run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]:
    """Evaluate every dialog with a fresh ``make_bot()`` instance and score turns in order.

    Example:
        run_dialog_eval(make_bot, [{"id": "d1", "turns": [...]}])
        # -> [{"dialog": "d1", "turn": 1, "ok": True, "reason": None}, ...]
    """
    # TODO:
    # 1. For each dialog in dialogs, call make_bot() once so history never leaks across dialogs.
    # 2. Ask each turn's question in order using bot.ask(turn["question"]).
    # 3. Score the reply with score_turn(reply, turn) and record
    #    {"dialog": dialog["id"], "turn": n, "ok": reason is None, "reason": reason} (n from 1).
    return None


def compare_to_baseline(
    current: list[dict],
    baseline: list[dict],
    min_pass_rate: float = 0.8,
) -> dict:
    """Compare ``current`` turn outcomes against ``baseline`` and compute the regression gate.

    Example:
        compare_to_baseline(
            [{"dialog": "d1", "turn": 1, "ok": True, "reason": None}],
            [{"dialog": "d1", "turn": 1, "ok": False, "reason": "refused"}],
        )
        # -> {
        #     "pass_rate": 1.0,
        #     "fixed": [("d1", 1)],
        #     "broken": [],
        #     "new": [],
        #     "failures": [],
        #     "gate_ok": True,
        # }
    """
    # TODO:
    # 1. Raise ValueError if current is empty.
    # 2. Index baseline by (dialog, turn).
    # 3. Walk current in order to build fixed, broken, new (not in baseline),
    #    and failures (dialog, turn, reason).
    # 4. Compute pass_rate = round(passed / len(current), 3).
    # 5. Compute gate_ok = not broken and pass_rate >= min_pass_rate and return the dict.
    return None
