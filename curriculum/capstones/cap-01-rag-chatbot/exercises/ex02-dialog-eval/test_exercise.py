import pytest
from exercise import REFUSAL, compare_to_baseline, run_dialog_eval, score_turn


class ScriptedBot:
    def __init__(self, replies: dict[str, dict]) -> None:
        self._replies = replies
        self.questions: list[str] = []

    def ask(self, question: str) -> dict:
        self.questions.append(question)
        return dict(self._replies[question])


class MemoryBot:
    def __init__(self) -> None:
        self.seen: list[str] = []

    def ask(self, question: str) -> dict:
        if question in self.seen:
            return {"answer": REFUSAL, "sources": [], "rewritten": question}
        self.seen.append(question)
        return {
            "answer": "Refunds are issued within 30 days of purchase. [1]",
            "sources": ["refunds.md"],
            "rewritten": question,
        }


def test_score_turn_refusal_rules():
    turn = {"question": "Do you take crypto?", "expected_source": None, "expected_facts": []}
    assert score_turn({"answer": REFUSAL, "sources": []}, turn) is None
    assert (
        score_turn({"answer": "We accept Visa only. [1]", "sources": ["payment.md"]}, turn)
        == "no_refusal"
    )
    assert (
        score_turn({"answer": REFUSAL, "sources": ["payment.md"]}, turn) == "no_refusal"
    ), "refusal turns must also return empty sources"


def test_score_turn_case_insensitive_facts():
    turn = {
        "question": "What about express?",
        "expected_source": "shipping.md",
        "expected_facts": ["express delivery", "12 DOLLARS"],
    }
    passing = {
        "answer": "EXPRESS DELIVERY arrives next day for 12 dollars. [1]",
        "sources": ["shipping.md"],
    }
    failing = {
        "answer": "EXPRESS DELIVERY arrives next day. [1]",
        "sources": ["shipping.md"],
    }
    assert score_turn(passing, turn) is None, "expected_facts check must be case-insensitive"
    assert score_turn(failing, turn) == "missing_fact"


@pytest.mark.parametrize(
    ("result", "turn", "expected_reason"),
    [
        (
            {"answer": REFUSAL, "sources": []},
            {
                "question": "How much is express?",
                "expected_source": "shipping.md",
                "expected_facts": ["12 dollars"],
            },
            "refused",
        ),
        (
            {"answer": "Express delivery costs 12 dollars. [1]", "sources": ["refunds.md"]},
            {
                "question": "How much is express?",
                "expected_source": "shipping.md",
                "expected_facts": ["12 dollars"],
            },
            "wrong_source",
        ),
        (
            {"answer": "Standard shipping takes 5 days. [1]", "sources": ["shipping.md"]},
            {
                "question": "How much is express?",
                "expected_source": "shipping.md",
                "expected_facts": ["12 dollars"],
            },
            "missing_fact",
        ),
        (
            {"answer": REFUSAL, "sources": ["shipping.md"]},
            {
                "question": "Do you take crypto?",
                "expected_source": None,
                "expected_facts": [],
            },
            "no_refusal",
        ),
    ],
)
def test_score_turn_failure_reasons_and_priority(result, turn, expected_reason):
    assert score_turn(result, turn) == expected_reason


def test_run_dialog_eval_calls_make_bot_once_per_dialog_and_isolates_history():
    created: list[MemoryBot] = []

    def make_bot():
        bot = MemoryBot()
        created.append(bot)
        return bot

    dialogs = [
        {
            "id": "d1",
            "turns": [
                {
                    "question": "How many days for refunds?",
                    "expected_source": "refunds.md",
                    "expected_facts": ["30 days"],
                }
            ],
        },
        {
            "id": "d2",
            "turns": [
                {
                    "question": "How many days for refunds?",
                    "expected_source": "refunds.md",
                    "expected_facts": ["30 days"],
                }
            ],
        },
    ]

    results = run_dialog_eval(make_bot, dialogs)
    assert len(created) == 2, "make_bot() must be called once per dialog"
    assert results == [
        {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d2", "turn": 1, "ok": True, "reason": None},
    ], "dialog histories must not leak across separate dialogs"


def test_run_dialog_eval_preserves_order_and_one_based_turns():
    bots: list[ScriptedBot] = []
    replies = {
        "How long is pickup held?": {
            "answer": "Unclaimed orders are held for 7 days. [1]",
            "sources": ["pickup.md"],
            "rewritten": "How long is pickup held?",
        },
        "And photo ID?": {
            "answer": "Wrong document answer. [1]",
            "sources": ["shipping.md"],
            "rewritten": "How long is pickup held? And photo ID?",
        },
        "Do you accept Bitcoin?": {
            "answer": REFUSAL,
            "sources": [],
            "rewritten": "Do you accept Bitcoin?",
        },
        "What about gift cards?": {
            "answer": "Gift cards work online. [1]",
            "sources": ["payment.md"],
            "rewritten": "What about gift cards?",
        },
    }

    def make_bot():
        bot = ScriptedBot(replies)
        bots.append(bot)
        return bot

    dialogs = [
        {
            "id": "dlg_alpha",
            "turns": [
                {
                    "question": "How long is pickup held?",
                    "expected_source": "pickup.md",
                    "expected_facts": ["7 days"],
                },
                {
                    "question": "And photo ID?",
                    "expected_source": "pickup.md",
                    "expected_facts": ["photo ID"],
                },
            ],
        },
        {
            "id": "dlg_beta",
            "turns": [
                {
                    "question": "Do you accept Bitcoin?",
                    "expected_source": None,
                    "expected_facts": [],
                },
                {
                    "question": "What about gift cards?",
                    "expected_source": "payment.md",
                    "expected_facts": ["cannot be redeemed"],
                },
            ],
        },
    ]

    results = run_dialog_eval(make_bot, dialogs)
    assert len(bots) == 2
    assert bots[0].questions == ["How long is pickup held?", "And photo ID?"]
    assert bots[1].questions == ["Do you accept Bitcoin?", "What about gift cards?"]
    assert results == [
        {"dialog": "dlg_alpha", "turn": 1, "ok": True, "reason": None},
        {"dialog": "dlg_alpha", "turn": 2, "ok": False, "reason": "wrong_source"},
        {"dialog": "dlg_beta", "turn": 1, "ok": True, "reason": None},
        {"dialog": "dlg_beta", "turn": 2, "ok": False, "reason": "missing_fact"},
    ]


def test_compare_to_baseline_tracks_fixed_broken_new_and_failures():
    baseline = [
        {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 2, "ok": False, "reason": "refused"},
        {"dialog": "d2", "turn": 1, "ok": True, "reason": None},
    ]
    current = [
        {"dialog": "d1", "turn": 1, "ok": False, "reason": "wrong_source"},
        {"dialog": "d1", "turn": 2, "ok": True, "reason": None},
        {"dialog": "d2", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d2", "turn": 2, "ok": False, "reason": "missing_fact"},
        {"dialog": "d3", "turn": 1, "ok": True, "reason": None},
    ]

    diff = compare_to_baseline(current, baseline)
    assert diff["pass_rate"] == 0.6
    assert diff["fixed"] == [("d1", 2)]
    assert diff["broken"] == [("d1", 1)], "failing new turns must not be counted in broken"
    assert diff["new"] == [("d2", 2), ("d3", 1)]
    assert diff["failures"] == [("d1", 1, "wrong_source"), ("d2", 2, "missing_fact")]
    assert diff["gate_ok"] is False


def test_compare_to_baseline_gate_fails_with_broken_despite_high_pass_rate():
    baseline = [
        {"dialog": "d1", "turn": n, "ok": True, "reason": None}
        for n in range(1, 6)
    ]
    current = [
        {"dialog": "d1", "turn": 1, "ok": False, "reason": "refused"},
        *[
            {"dialog": "d1", "turn": n, "ok": True, "reason": None}
            for n in range(2, 6)
        ],
    ]

    diff = compare_to_baseline(current, baseline, min_pass_rate=0.5)
    assert diff["pass_rate"] == 0.8
    assert diff["broken"] == [("d1", 1)]
    assert diff["gate_ok"] is False, "any broken turn must fail the regression gate"


def test_compare_to_baseline_gate_fails_below_min_pass_rate():
    baseline = [
        {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 2, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 3, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 4, "ok": False, "reason": "refused"},
    ]
    current = [dict(row) for row in baseline]

    diff = compare_to_baseline(current, baseline, min_pass_rate=0.8)
    assert diff["broken"] == []
    assert diff["pass_rate"] == 0.75
    assert diff["gate_ok"] is False


def test_compare_to_baseline_gate_passes_at_exact_threshold_and_rounds_pass_rate():
    baseline = [
        {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 2, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 3, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 4, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 5, "ok": False, "reason": "missing_fact"},
    ]
    current = [dict(row) for row in baseline]

    boundary = compare_to_baseline(current, baseline, min_pass_rate=0.8)
    assert boundary["pass_rate"] == 0.8
    assert boundary["broken"] == []
    assert boundary["gate_ok"] is True, "pass_rate == min_pass_rate must pass the gate"

    three_turns = [
        {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 2, "ok": True, "reason": None},
        {"dialog": "d1", "turn": 3, "ok": False, "reason": "no_refusal"},
    ]
    rounded = compare_to_baseline(three_turns, three_turns, min_pass_rate=0.6)
    assert rounded["pass_rate"] == 0.667
    assert rounded["gate_ok"] is True


def test_compare_to_baseline_empty_current_raises_value_error():
    baseline = [{"dialog": "d1", "turn": 1, "ok": True, "reason": None}]
    with pytest.raises(ValueError):
        compare_to_baseline([], baseline)
