import pytest
from fastapi.testclient import TestClient
from pyai_llm import FakeLLM

import exercise

DOCS = [
    {
        "id": "refunds",
        "text": "Refunds take 5 business days after approval. Keep your receipt.",
    },
    {
        "id": "shipping",
        "text": (
            "Express shipping costs 12 dollars and arrives next day. "
            "Free shipping starts at 50 dollars."
        ),
    },
    {
        "id": "warranty",
        "text": "Hardware warranty covers factory defects for 12 months. Water damage is excluded.",
    },
    {
        "id": "support",
        "text": (
            "Support agents work Monday to Friday from 9 AM to 6 PM. "
            "Urgent tickets get priority."
        ),
    },
    {
        "id": "security",
        "text": "Two-factor login protects your account. Password resets arrive by email.",
    },
    {
        "id": "billing",
        "text": "Invoices are emailed right after checkout. Accepted cards include Visa.",
    },
]


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class SlowClient:
    def __init__(self, inner: FakeLLM, clock: FakeClock) -> None:
        self.inner = inner
        self.clock = clock
        self.embed_calls = 0
        self.chat_calls = 0
        self.last_usage: tuple[int, int] | None = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls += 1
        return self.inner.embed(texts)

    def chat(self, messages: list[dict]):
        self.chat_calls += 1
        resp = self.inner.chat(messages)
        # Fixed latency formula: 0.2s base + 0.002s per completion token
        self.clock.advance(0.2 + 0.002 * resp.usage.completion_tokens)
        self.last_usage = (resp.usage.prompt_tokens, resp.usage.completion_tokens)
        return resp


@pytest.fixture
def harness():
    clock = FakeClock()
    client = SlowClient(FakeLLM(embed_dim=256), clock)
    app = exercise.create_app(
        DOCS,
        client,
        clock,
        cache_ttl=300.0,
        price_in_per_1k=0.0005,
        price_out_per_1k=0.0015,
    )
    return TestClient(app), client, clock


def test_repeat_question_hits_cache_and_skips_chat(harness):
    http, client, _ = harness
    r1 = http.post("/ask", json={"question": "How many days do refunds take?"})
    r2 = http.post("/ask", json={"question": "How many days do refunds take?"})
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["cached"] is False
    assert r2.json()["cached"] is True
    assert r2.json()["usage"] == {"prompt_tokens": 0, "completion_tokens": 0}
    assert r2.json()["answer"] == r1.json()["answer"]
    assert client.chat_calls == 1


def test_whitespace_normalization_hits_cache(harness):
    http, client, _ = harness
    http.post("/ask", json={"question": "How many days do refunds take?"})
    r2 = http.post("/ask", json={"question": "  How many days   do refunds take?  "})
    assert r2.json()["cached"] is True
    assert client.chat_calls == 1


def test_different_top_k_misses_cache(harness):
    http, client, _ = harness
    r1 = http.post("/ask", json={"question": "How many days do refunds take?", "top_k": 2})
    r2 = http.post("/ask", json={"question": "How many days do refunds take?", "top_k": 1})
    assert r1.json()["cached"] is False
    assert r2.json()["cached"] is False
    assert client.chat_calls == 2


def test_ttl_expiration_at_exact_boundary_is_miss(harness):
    http, client, clock = harness
    r1 = http.post("/ask", json={"question": "How many days do refunds take?"})
    assert r1.json()["cached"] is False

    clock.advance(299.0)
    r2 = http.post("/ask", json={"question": "How many days do refunds take?"})
    assert r2.json()["cached"] is True

    clock.advance(1.0)
    r3 = http.post("/ask", json={"question": "How many days do refunds take?"})
    assert r3.json()["cached"] is False
    assert client.chat_calls == 2


def test_refusal_is_cached_without_re_embedding(harness):
    http, client, _ = harness
    r1 = http.post("/ask", json={"question": "Can I pay with crypto?"})
    embeds_after_first = client.embed_calls
    r2 = http.post("/ask", json={"question": "Can I pay with crypto?"})
    assert r1.json()["sources"] == []
    assert r1.json()["cached"] is False
    assert r2.json()["cached"] is True
    assert r2.json()["sources"] == []
    assert client.chat_calls == 0
    assert client.embed_calls == embeds_after_first


def test_empty_metrics_returns_zeros(harness):
    http, _, _ = harness
    r = http.get("/metrics")
    assert r.status_code == 200
    assert r.json() == {"requests": 0, "cache_hit_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}


def test_metrics_counts_requests_and_cache_hit_rate(harness):
    http, _, _ = harness
    http.post("/ask", json={"question": "How many days do refunds take?"})
    http.post("/ask", json={"question": "How many days do refunds take?"})
    http.post("/ask", json={"question": "How long is hardware warranty?"})
    m = http.get("/metrics").json()
    assert m["requests"] == 3
    assert m["cache_hit_rate"] == pytest.approx(1 / 3)


def test_metrics_computes_nearest_rank_p95_ms(harness):
    http, client, _ = harness
    r1 = http.post("/ask", json={"question": "How many days do refunds take?"})
    c1 = r1.json()["usage"]["completion_tokens"]
    expected_ms_1 = (0.2 + 0.002 * c1) * 1000.0
    http.post("/ask", json={"question": "How many days do refunds take?"})
    m = http.get("/metrics").json()
    assert m["p95_ms"] == pytest.approx(expected_ms_1)
    assert client.chat_calls == 1


def test_metrics_total_cost_matches_sum_and_cache_hits_cost_zero(harness):
    http, _, _ = harness
    r1 = http.post("/ask", json={"question": "How many days do refunds take?"})
    u1 = r1.json()["usage"]
    c1 = (u1["prompt_tokens"] / 1000.0) * 0.0005 + (u1["completion_tokens"] / 1000.0) * 0.0015
    cost_after_first = http.get("/metrics").json()["total_cost"]
    assert cost_after_first == pytest.approx(round(c1, 6))

    http.post("/ask", json={"question": "How many days do refunds take?"})
    assert http.get("/metrics").json()["total_cost"] == pytest.approx(round(c1, 6))

    r3 = http.post("/ask", json={"question": "How long is hardware warranty?"})
    u3 = r3.json()["usage"]
    c3 = (u3["prompt_tokens"] / 1000.0) * 0.0005 + (u3["completion_tokens"] / 1000.0) * 0.0015
    assert http.get("/metrics").json()["total_cost"] == pytest.approx(round(c1 + c3, 6))
