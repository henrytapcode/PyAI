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


class SpyClient:
    def __init__(self, inner: FakeLLM) -> None:
        self.inner = inner
        self.embed_batches: list[list[str]] = []
        self.chat_calls = 0
        self.last_messages: list[dict] = []
        self.last_usage: dict[str, int] | None = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_batches.append(list(texts))
        return self.inner.embed(texts)

    def chat(self, messages: list[dict]):
        self.chat_calls += 1
        self.last_messages = list(messages)
        resp = self.inner.chat(messages)
        self.last_usage = {
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
        }
        return resp


@pytest.fixture
def harness():
    spy = SpyClient(FakeLLM(embed_dim=256))
    app = exercise.create_app(DOCS, spy, min_score=0.2)
    return TestClient(app), spy


def test_health_reports_ok_and_doc_count(harness):
    client, _ = harness
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "docs": len(DOCS)}


def test_get_document_found_and_missing(harness):
    client, _ = harness
    ok = client.get("/documents/refunds")
    assert ok.status_code == 200
    assert ok.json() == DOCS[0]

    missing = client.get("/documents/unknown-id")
    assert missing.status_code == 404
    assert missing.json() == {"detail": "document not found"}


def test_embed_called_once_for_corpus_despite_many_requests(harness):
    client, spy = harness
    assert len(spy.embed_batches) == 1
    assert spy.embed_batches[0] == [d["text"] for d in DOCS]

    for q in [
        "How many days do refunds take?",
        "How much does express shipping cost?",
        "How long is hardware warranty?",
    ]:
        r = client.post("/ask", json={"question": q})
        assert r.status_code == 200

    doc_batches = [b for b in spy.embed_batches if len(b) == len(DOCS)]
    assert len(doc_batches) == 1, "documents must be embedded only once in create_app"


def test_ask_returns_answer_ordered_sources_and_rounded_scores(harness):
    client, _ = harness
    r = client.post("/ask", json={"question": "How many days do refunds take?"})
    assert r.status_code == 200
    data = r.json()
    assert data["sources"] == ["refunds"]
    assert data["scores"] == [0.387]
    assert "5 business days" in data["answer"]


def test_ask_respects_top_k_and_exact_non_alphabetical_order():
    spy = SpyClient(FakeLLM(embed_dim=256))
    client = TestClient(exercise.create_app(DOCS, spy, min_score=0.0))

    r3 = client.post(
        "/ask",
        json={"question": "Express shipping costs 12 dollars?", "top_k": 3},
    )
    assert r3.status_code == 200
    data = r3.json()
    assert data["sources"] == ["shipping", "warranty", "support"]
    assert data["scores"] == [0.683, 0.129, 0.1]
    assert len(data["sources"]) == 3

    combined = "\n".join(m["content"] for m in spy.last_messages)
    assert f"[1] {DOCS[1]['text']}" in combined
    assert f"[2] {DOCS[2]['text']}" in combined
    assert f"[3] {DOCS[3]['text']}" in combined


def test_ask_refusal_below_min_score_skips_chat(harness):
    client, spy = harness
    r = client.post("/ask", json={"question": "Can I pay with crypto?"})
    assert r.status_code == 200
    assert r.json() == {
        "answer": "I don't know based on the provided context.",
        "sources": [],
        "scores": [],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0},
    }
    assert spy.chat_calls == 0


def test_ask_clears_sources_and_scores_when_model_refuses():
    spy = SpyClient(
        FakeLLM(
            embed_dim=256,
            script=["I don't know based on the provided context."],
        )
    )
    client = TestClient(exercise.create_app(DOCS, spy, min_score=0.2))
    r = client.post("/ask", json={"question": "How many days do refunds take?"})
    assert r.status_code == 200
    data = r.json()
    assert spy.chat_calls == 1
    assert data["answer"] == "I don't know based on the provided context."
    assert data["sources"] == []
    assert data["scores"] == []
    assert data["usage"] == spy.last_usage


def test_ask_passes_numbered_context_and_returns_usage():
    spy = SpyClient(FakeLLM(embed_dim=256))
    client = TestClient(exercise.create_app(DOCS, spy, min_score=0.0))
    r = client.post("/ask", json={"question": "How long is hardware warranty?", "top_k": 2})
    assert r.status_code == 200
    data = r.json()
    assert spy.chat_calls == 1
    combined = "\n".join(m["content"] for m in spy.last_messages)
    assert "Context:" in combined
    assert f"[1] {DOCS[2]['text']}" in combined
    assert f"[2] {DOCS[0]['text']}" in combined
    assert data["usage"] == spy.last_usage


def test_ask_tie_breaks_by_original_doc_order():
    tied_docs = [
        {"id": "first", "text": "Warranty covers defects."},
        {"id": "second", "text": "Warranty covers defects."},
    ]
    spy = SpyClient(FakeLLM(embed_dim=256))
    client = TestClient(exercise.create_app(tied_docs, spy, min_score=0.2))
    r = client.post("/ask", json={"question": "Warranty covers defects?", "top_k": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["sources"] == ["first", "second"]
    assert data["scores"] == [1.0, 1.0]


@pytest.mark.parametrize(
    "payload",
    [
        {"question": ""},
        {"question": "Refunds?", "top_k": 9},
    ],
)
def test_ask_rejects_invalid_payloads_with_422(harness, payload):
    client, _ = harness
    r = client.post("/ask", json=payload)
    assert r.status_code == 422


def test_two_apps_do_not_share_state():
    spy_a = SpyClient(FakeLLM(embed_dim=256))
    spy_b = SpyClient(FakeLLM(embed_dim=256))
    app_a = TestClient(exercise.create_app(DOCS[:2], spy_a, min_score=0.2))
    app_b = TestClient(exercise.create_app(DOCS[2:5], spy_b, min_score=0.9))

    assert app_a.get("/health").json()["docs"] == 2
    assert app_b.get("/health").json()["docs"] == 3
    r_a = app_a.post("/ask", json={"question": "How many days do refunds take?"})
    assert r_a.json()["sources"] == ["refunds"]
    r_b = app_b.post("/ask", json={"question": "How long is hardware warranty?"})
    assert r_b.json()["sources"] == []
