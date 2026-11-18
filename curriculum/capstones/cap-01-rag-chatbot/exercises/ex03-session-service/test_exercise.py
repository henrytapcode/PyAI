import pytest
from exercise import create_app
from fastapi.testclient import TestClient


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


class EchoBot:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def ask(self, question: str) -> dict:
        self.questions.append(question)
        return {
            "answer": f"echo: {question}",
            "sources": [],
            "rewritten": question,
        }


class BotFactory:
    def __init__(self) -> None:
        self.bots: list[EchoBot] = []

    def __call__(self) -> EchoBot:
        bot = EchoBot()
        self.bots.append(bot)
        return bot


@pytest.fixture
def harness():
    clock = FakeClock()
    factory = BotFactory()
    app = create_app(factory, clock, session_ttl=60.0, max_sessions=2)
    return TestClient(app), clock, factory


def test_health_and_create_sessions_return_201_with_sequential_ids(harness):
    client, _, factory = harness
    h0 = client.get("/health")
    assert h0.status_code == 200
    assert h0.json() == {"status": "ok", "active_sessions": 0}

    r1 = client.post("/sessions")
    assert r1.status_code == 201
    assert r1.json() == {"session_id": "s1"}

    r2 = client.post("/sessions")
    assert r2.status_code == 201
    assert r2.json() == {"session_id": "s2"}

    assert len(factory.bots) == 2
    assert client.get("/health").json() == {"status": "ok", "active_sessions": 2}


def test_each_session_gets_isolated_bot_instance(harness):
    client, _, factory = harness
    client.post("/sessions")
    client.post("/sessions")

    r1 = client.post("/sessions/s1/messages", json={"question": "shipping cost?"})
    r2 = client.post("/sessions/s2/messages", json={"question": "refund window?"})

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert len(factory.bots) == 2
    assert factory.bots[0] is not factory.bots[1]
    assert factory.bots[0].questions == ["shipping cost?"]
    assert factory.bots[1].questions == ["refund window?"]


def test_messages_increment_turn_and_get_session_returns_turns(harness):
    client, _, _ = harness
    client.post("/sessions")

    t1 = client.post("/sessions/s1/messages", json={"question": "First?"})
    assert t1.status_code == 200
    assert t1.json() == {
        "answer": "echo: First?",
        "sources": [],
        "rewritten": "First?",
        "turn": 1,
    }

    t2 = client.post("/sessions/s1/messages", json={"question": "Second?"})
    assert t2.status_code == 200
    assert t2.json() == {
        "answer": "echo: Second?",
        "sources": [],
        "rewritten": "Second?",
        "turn": 2,
    }

    hist = client.get("/sessions/s1")
    assert hist.status_code == 200
    assert hist.json() == {
        "session_id": "s1",
        "turns": [
            {"question": "First?", "answer": "echo: First?"},
            {"question": "Second?", "answer": "echo: Second?"},
        ],
    }


def test_session_expires_at_exact_ttl_boundary_across_routes():
    clock = FakeClock()
    client = TestClient(create_app(BotFactory(), clock, session_ttl=10.0, max_sessions=5))
    client.post("/sessions")

    clock.advance(9.0)
    assert client.get("/sessions/s1").status_code == 200

    clock.advance(10.0)
    expired_get = client.get("/sessions/s1")
    assert expired_get.status_code == 404
    assert expired_get.json() == {"detail": "session not found"}

    expired_msg = client.post("/sessions/s1/messages", json={"question": "Still alive?"})
    assert expired_msg.status_code == 404
    assert expired_msg.json() == {"detail": "session not found"}
    assert client.get("/health").json() == {"status": "ok", "active_sessions": 0}


def test_health_and_post_messages_purge_expired_sessions():
    clock = FakeClock()
    client = TestClient(create_app(BotFactory(), clock, session_ttl=10.0, max_sessions=2))
    client.post("/sessions")

    clock.advance(10.0)
    assert client.get("/health").json() == {"status": "ok", "active_sessions": 0}
    assert client.post("/sessions/s1/messages", json={"question": "Hello?"}).status_code == 404


def test_get_and_post_refresh_last_seen_before_expiry():
    clock = FakeClock()
    client = TestClient(create_app(BotFactory(), clock, session_ttl=10.0, max_sessions=5))
    client.post("/sessions")

    clock.advance(6.0)
    assert client.get("/sessions/s1").status_code == 200

    clock.advance(6.0)
    r = client.post("/sessions/s1/messages", json={"question": "Still here?"})
    assert r.status_code == 200

    clock.advance(6.0)
    assert client.get("/sessions/s1").status_code == 200


def test_evicts_least_recently_used_session_at_capacity():
    clock = FakeClock()
    client = TestClient(create_app(BotFactory(), clock, session_ttl=100.0, max_sessions=2))
    client.post("/sessions")  # s1 at t=0
    clock.advance(1.0)
    client.post("/sessions")  # s2 at t=1
    clock.advance(1.0)
    assert client.get("/sessions/s1").status_code == 200  # refresh s1 at t=2; s2 is LRU

    clock.advance(1.0)
    s3 = client.post("/sessions")  # s3 at t=3 -> evict s2
    assert s3.status_code == 201
    assert s3.json() == {"session_id": "s3"}
    assert client.get("/sessions/s2").status_code == 404
    assert client.get("/sessions/s1").status_code == 200
    assert client.get("/sessions/s3").status_code == 200


def test_eviction_tie_breaks_by_creation_order():
    clock = FakeClock()
    client = TestClient(create_app(BotFactory(), clock, session_ttl=100.0, max_sessions=2))
    client.post("/sessions")  # s1 at t=0
    client.post("/sessions")  # s2 at t=0
    client.post("/sessions")  # s3 at t=0 -> s1 created earlier, so s1 evicted

    assert client.get("/sessions/s1").status_code == 404
    assert client.get("/sessions/s2").status_code == 200
    assert client.get("/sessions/s3").status_code == 200


def test_missing_session_returns_404_on_both_routes(harness):
    client, _, _ = harness
    r_get = client.get("/sessions/does-not-exist")
    assert r_get.status_code == 404
    assert r_get.json() == {"detail": "session not found"}

    r_post = client.post("/sessions/does-not-exist/messages", json={"question": "Hello?"})
    assert r_post.status_code == 404
    assert r_post.json() == {"detail": "session not found"}


@pytest.mark.parametrize("bad_question", ["", "   \t\n"])
def test_blank_and_whitespace_questions_return_422(harness, bad_question):
    client, _, _ = harness
    client.post("/sessions")
    r = client.post("/sessions/s1/messages", json={"question": bad_question})
    assert r.status_code == 422


def test_two_apps_have_isolated_session_stores():
    clock = FakeClock()
    client_a = TestClient(create_app(BotFactory(), clock, session_ttl=60.0, max_sessions=5))
    client_b = TestClient(create_app(BotFactory(), clock, session_ttl=60.0, max_sessions=5))

    assert client_a.post("/sessions").json() == {"session_id": "s1"}
    assert client_a.post("/sessions/s1/messages", json={"question": "Only in A"}).status_code == 200

    assert client_b.get("/health").json() == {"status": "ok", "active_sessions": 0}
    assert client_b.get("/sessions/s1").status_code == 404


@pytest.mark.parametrize(
    ("ttl", "limit"),
    [(0.0, 2), (-1.0, 2), (60.0, 0), (60.0, -3)],
)
def test_invalid_config_raises_value_error(ttl, limit):
    with pytest.raises(ValueError):
        create_app(BotFactory(), FakeClock(), session_ttl=ttl, max_sessions=limit)
