import pytest
from fastapi.testclient import TestClient

import exercise


@pytest.fixture
def client():
    return TestClient(exercise.app)


def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}, "GET /health must return {'status': 'ok'}"


def test_ask_ranks_sources_by_overlap_and_tiebreaks_by_id(client):
    r = client.post("/ask", json={"question": "FastAPI tests", "top_k": 5})
    assert r.status_code == 200
    body = r.json()
    assert body is not None, "ask returned None: did you forget to return the response dict?"
    assert body == {"question": "FastAPI tests", "sources": [3, 4, 1]}


def test_ask_limits_sources_to_top_k(client):
    r = client.post("/ask", json={"question": "FastAPI tests", "top_k": 1})
    assert r.status_code == 200
    body = r.json()
    assert body is not None, "ask returned None: did you forget to return the response dict?"
    assert body["sources"] == [3]


def test_ask_returns_404_when_no_documents_match(client):
    r = client.post("/ask", json={"question": "unknown topic"})
    assert r.status_code == 404, "raise HTTPException(status_code=404, ...) when nothing matches"
    assert r.json()["detail"] == "no matching documents"


@pytest.mark.parametrize(
    "payload",
    [
        {"question": ""},
        {"question": "FastAPI", "top_k": 9},
    ],
)
def test_ask_rejects_invalid_payloads_with_422(client, payload):
    r = client.post("/ask", json=payload)
    assert r.status_code == 422, "check Field constraints on AskRequest"


def test_ask_defaults_top_k_to_two(client):
    r = client.post("/ask", json={"question": "FastAPI"})
    assert r.status_code == 200
    body = r.json()
    assert body is not None, "ask returned None: did you forget to return the response dict?"
    assert body["sources"] == [1, 3]
