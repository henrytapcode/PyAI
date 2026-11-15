import pytest
from exercise import evaluate_bot, report_lines


def _make_bot(responses: dict[str, dict]):
    def bot(question: str) -> dict:
        return dict(responses[question])

    return bot


def test_perfect_bot_returns_full_counts_and_no_failures():
    eval_set = [
        {"id": "q1", "question": "Q1?", "expected_source": "a.md", "expected_facts": ["30 days"]},
        {"id": "q2", "question": "Q2?", "expected_source": None, "expected_facts": []},
    ]
    bot = _make_bot({
        "Q1?": {
            "answer": "Refunds take 30 days. [1]",
            "sources": ["a.md"],
            "retrieved": ["a.md", "b.md"],
        },
        "Q2?": {"answer": "I don't know based on context.", "sources": [], "retrieved": []},
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary == {
        "n": 2,
        "hits": 1,
        "n_answerable": 1,
        "facts_ok": 1,
        "idk_ok": 1,
        "n_unanswerable": 1,
        "failures": [],
    }


def test_retrieval_miss_prioritized_even_if_facts_match():
    eval_set = [
        {
            "id": "q1",
            "question": "Q1?",
            "expected_source": "refunds.md",
            "expected_facts": ["30 days"],
        },
    ]
    bot = _make_bot({
        "Q1?": {"answer": "Takes 30 days.", "sources": ["other.md"], "retrieved": ["other.md"]},
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary["hits"] == 0
    assert summary["facts_ok"] == 1
    assert summary["failures"] == [("q1", "retrieval_miss")]


def test_answer_miss_recorded_when_retrieval_hits_but_fact_missing():
    eval_set = [
        {
            "id": "q1",
            "question": "Q1?",
            "expected_source": "refunds.md",
            "expected_facts": ["30 days", "receipt"],
        },
    ]
    bot = _make_bot({
        "Q1?": {
            "answer": "Refunds take 30 DAYS. [1]",
            "sources": ["refunds.md"],
            "retrieved": ["refunds.md"],
        },
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary["hits"] == 1
    assert summary["facts_ok"] == 0
    assert summary["failures"] == [("q1", "answer_miss")]


def test_unanswerable_without_idk_phrase_records_no_refusal():
    eval_set = [
        {"id": "q1", "question": "Crypto?", "expected_source": None, "expected_facts": []},
    ]
    bot = _make_bot({
        "Crypto?": {
            "answer": "We accept Visa. [1]",
            "sources": ["payment.md"],
            "retrieved": ["payment.md"],
        },
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary["idk_ok"] == 0
    assert summary["n_unanswerable"] == 1
    assert summary["failures"] == [("q1", "no_refusal")]


def test_unanswerable_with_idk_and_nonempty_sources_records_no_refusal():
    eval_set = [
        {"id": "q1", "question": "Crypto?", "expected_source": None, "expected_facts": []},
    ]
    bot = _make_bot({
        "Crypto?": {
            "answer": "I don't know.",
            "sources": ["payment.md"],
            "retrieved": ["payment.md"],
        },
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary["idk_ok"] == 0
    assert summary["failures"] == [("q1", "no_refusal")]


def test_failures_preserve_eval_set_order():
    eval_set = [
        {"id": "q1", "question": "Q1?", "expected_source": "a.md", "expected_facts": ["f1"]},
        {"id": "q2", "question": "Q2?", "expected_source": "b.md", "expected_facts": ["f2"]},
        {"id": "q3", "question": "Q3?", "expected_source": None, "expected_facts": []},
        {"id": "q4", "question": "Q4?", "expected_source": "c.md", "expected_facts": ["f4"]},
    ]
    bot = _make_bot({
        "Q1?": {"answer": "f1", "sources": ["a.md"], "retrieved": ["a.md"]},
        "Q2?": {"answer": "nope", "sources": ["b.md"], "retrieved": ["b.md"]},
        "Q3?": {"answer": "Sure!", "sources": ["c.md"], "retrieved": ["c.md"]},
        "Q4?": {"answer": "nope", "sources": [], "retrieved": ["other.md"]},
    })
    summary = evaluate_bot(bot, eval_set)
    assert summary["failures"] == [
        ("q2", "answer_miss"),
        ("q3", "no_refusal"),
        ("q4", "retrieval_miss"),
    ]


def test_evaluate_bot_does_not_mutate_eval_set():
    eval_set = [
        {"id": "q1", "question": "Q1?", "expected_source": "a.md", "expected_facts": ["30 days"]},
    ]
    snapshot = [dict(eval_set[0], expected_facts=list(eval_set[0]["expected_facts"]))]
    bot = _make_bot({"Q1?": {"answer": "30 days", "sources": ["a.md"], "retrieved": ["a.md"]}})
    summary = evaluate_bot(bot, eval_set)
    assert isinstance(summary, dict) and summary["n"] == 1
    assert eval_set == snapshot


def test_report_lines_formats_metrics_and_failures():
    summary = {
        "n": 7,
        "hits": 4,
        "n_answerable": 5,
        "facts_ok": 3,
        "idk_ok": 1,
        "n_unanswerable": 2,
        "failures": [("q3", "answer_miss"), ("q6", "no_refusal")],
    }
    assert report_lines(summary) == [
        "hit@k: 4/5 (80%)",
        "facts: 3/5 (60%)",
        "refusals: 1/2 (50%)",
        "FAIL q3: answer_miss",
        "FAIL q6: no_refusal",
        "failures: 2",
    ]


@pytest.mark.parametrize(
    ("summary", "expected"),
    [
        (
            {
                "n": 1, "hits": 0, "n_answerable": 0, "facts_ok": 0,
                "idk_ok": 1, "n_unanswerable": 1, "failures": [],
            },
            ["hit@k: n/a", "facts: n/a", "refusals: 1/1 (100%)", "failures: 0"],
        ),
        (
            {
                "n": 2, "hits": 1, "n_answerable": 2, "facts_ok": 1,
                "idk_ok": 0, "n_unanswerable": 0, "failures": [("q2", "retrieval_miss")],
            },
            [
                "hit@k: 1/2 (50%)",
                "facts: 1/2 (50%)",
                "refusals: n/a",
                "FAIL q2: retrieval_miss",
                "failures: 1",
            ],
        ),
    ],
)
def test_report_lines_handles_zero_denominators(summary, expected):
    assert report_lines(summary) == expected
