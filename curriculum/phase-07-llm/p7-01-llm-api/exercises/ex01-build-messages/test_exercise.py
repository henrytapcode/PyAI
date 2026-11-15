import pytest
from exercise import build_messages
from pyai_llm import FakeLLM


def test_empty_history_returns_system_and_user():
    msgs = build_messages("Be concise.", [], "What is RAG?")
    assert msgs is not None, "build_messages returned None: did you forget to return the list?"
    assert msgs == [
        {"role": "system", "content": "Be concise."},
        {"role": "user", "content": "What is RAG?"},
    ]


def test_preserves_role_order_with_history():
    history = [("Hello", "Hi!"), ("What is a token?", "A piece of text.")]
    msgs = build_messages("You are a tutor.", history, "What is RAG?")
    assert msgs is not None, "build_messages returned None: did you forget to return the list?"
    roles = [m["role"] for m in msgs]
    assert roles == ["system", "user", "assistant", "user", "assistant", "user"]


def test_preserves_exact_contents_without_mutating_history():
    history = [("First question", "First answer")]
    original = list(history)
    msgs = build_messages("System rules", history, "Follow-up question")
    assert msgs is not None, "build_messages returned None: did you forget to return the list?"
    assert [m["content"] for m in msgs] == [
        "System rules",
        "First question",
        "First answer",
        "Follow-up question",
    ]
    assert history == original, "do not modify the input history list in place"


@pytest.mark.parametrize("turns", [0, 1, 2, 3])
def test_length_matches_expected_formula(turns: int):
    history = [(f"q{i}", f"a{i}") for i in range(turns)]
    msgs = build_messages("Sys", history, "New question")
    assert msgs is not None, "build_messages returned None: did you forget to return the list?"
    assert len(msgs) == 1 + 2 * len(history) + 1


def test_messages_run_cleanly_in_fake_llm():
    history = [("Hi", "Hello!")]
    msgs = build_messages("You are helpful.", history, "What is RAG?")
    assert msgs is not None, "build_messages returned None: did you forget to return the list?"
    resp = FakeLLM().chat(msgs)
    assert resp.finish_reason == "stop"
    assert isinstance(resp.content, str) and len(resp.content) > 0
