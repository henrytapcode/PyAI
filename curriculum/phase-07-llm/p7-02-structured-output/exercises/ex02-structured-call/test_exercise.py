import pytest
from exercise import get_ticket, parse_reply
from pyai_llm import ChatResponse, FakeLLM

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "order_id": {"type": "integer"},
        "urgent": {"type": "boolean"},
    },
    "required": ["name", "order_id", "urgent"],
}


class _SpyClient:
    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.recorded_messages: list[list[dict[str, str]]] = []
        self.calls = 0

    def chat(
        self,
        messages: list[dict[str, str]],
        response_format: dict | None = None,
    ) -> ChatResponse:
        assert response_format == {"type": "json", "schema": SCHEMA}
        self.recorded_messages.append([dict(m) for m in messages])
        reply = self._replies[self.calls]
        self.calls += 1
        return ChatResponse(content=reply)


def test_parse_reply_plain_json():
    parsed = parse_reply('{"name": "Lan", "order_id": 1042, "urgent": true}')
    assert parsed is not None, "parse_reply returned None: did you forget to return the dict?"
    assert parsed == {"name": "Lan", "order_id": 1042, "urgent": True}


def test_parse_reply_strips_fence_and_prose():
    noisy = (
        'Sure! Here is the JSON:\n```json\n'
        '{"name": "Minh", "order_id": 205, "urgent": false}\n```\nHope that helps.'
    )
    parsed = parse_reply(noisy)
    assert parsed is not None, "parse_reply returned None: did you forget to return the dict?"
    assert parsed == {"name": "Minh", "order_id": 205, "urgent": False}


def test_parse_reply_raises_without_json():
    with pytest.raises(ValueError):
        parse_reply("Sorry, I cannot extract a ticket from this message.")


def test_get_ticket_succeeds_on_first_attempt():
    client = FakeLLM()
    msgs = [{"role": "user", "content": "name: Lan, order_id: 1042, urgent: yes"}]
    result = get_ticket(client, msgs, SCHEMA, max_attempts=3)
    assert result is not None, "get_ticket returned None: forgot to return (data, attempts)?"
    data, attempts = result
    assert attempts == 1
    assert data == {"name": "Lan", "order_id": 1042, "urgent": True}


def test_get_ticket_retries_once_then_succeeds():
    client = FakeLLM(script=[
        '{"name": "Lan", "order_id": "bad", "urgent": true}',
        '{"name": "Lan", "order_id": 1042, "urgent": true}',
    ])
    msgs = [{"role": "user", "content": "name: Lan, order_id: 1042, urgent: yes"}]
    result = get_ticket(client, msgs, SCHEMA, max_attempts=3)
    assert result is not None, "get_ticket returned None: forgot to return (data, attempts)?"
    data, attempts = result
    assert attempts == 2
    assert data == {"name": "Lan", "order_id": 1042, "urgent": True}


def test_get_ticket_exhausts_attempts_returns_none():
    client = FakeLLM(script=[
        "not json at all",
        '{"name": "Lan"}',
        '{"name": "Lan", "order_id": true, "urgent": false}',
    ])
    msgs = [{"role": "user", "content": "ticket"}]
    result = get_ticket(client, msgs, SCHEMA, max_attempts=3)
    assert result is not None, "get_ticket returned None: forgot to return (None, max_attempts)?"
    assert result == (None, 3)


def test_get_ticket_does_not_mutate_messages():
    client = FakeLLM(script=[
        '{"name": "Lan"}',
        '{"name": "Lan", "order_id": 1042, "urgent": true}',
    ])
    msgs = [{"role": "user", "content": "ticket"}]
    snapshot = [dict(m) for m in msgs]
    result = get_ticket(client, msgs, SCHEMA, max_attempts=3)
    assert result is not None, "get_ticket returned None: forgot to return (data, attempts)?"
    assert len(msgs) == 1
    assert msgs == snapshot, "do not mutate the caller's original messages list"


def test_get_ticket_sends_error_feedback_on_retry():
    bad_reply = '{"name": "Lan", "urgent": true}'
    good_reply = '{"name": "Lan", "order_id": 1042, "urgent": true}'
    spy = _SpyClient([bad_reply, good_reply])
    msgs = [{"role": "user", "content": "ticket"}]
    result = get_ticket(spy, msgs, SCHEMA, max_attempts=3)
    assert result == ({"name": "Lan", "order_id": 1042, "urgent": True}, 2)
    assert len(spy.recorded_messages) == 2
    second_call = spy.recorded_messages[1]
    assert len(second_call) == 3
    assert second_call[1] == {"role": "assistant", "content": bad_reply}
    assert second_call[2]["role"] == "user"
    assert "order_id" in second_call[2]["content"]
