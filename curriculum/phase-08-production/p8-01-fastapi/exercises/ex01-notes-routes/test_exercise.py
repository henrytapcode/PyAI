import pytest
from fastapi.testclient import TestClient

import exercise


@pytest.fixture
def client():
    exercise.notes.clear()
    return TestClient(exercise.app)


def test_list_notes_returns_a_list(client):
    r = client.get("/notes")
    assert r.status_code == 200
    assert r.json() == []
    client.post("/notes", json={"text": "first note"})
    r_after = client.get("/notes")
    assert r_after.status_code == 200
    assert r_after.json() == [{"id": 1, "text": "first note"}]


def test_create_note_returns_201_with_new_id(client):
    r = client.post("/notes", json={"text": "ship v1"})
    assert r.status_code == 201, "creating a note must return status 201"
    assert r.json() == {"id": 1, "text": "ship v1"}


def test_get_missing_note_returns_404(client):
    r = client.get("/notes/999")
    assert r.status_code == 404, "missing note ID must raise 404"


def test_get_non_integer_note_id_returns_422(client):
    r = client.get("/notes/abc")
    assert r.status_code == 422, "non-integer note_id must fail validation with 422"


def test_create_note_missing_text_returns_422(client):
    r = client.post("/notes", json={})
    assert r.status_code == 422, "payload without 'text' must fail validation with 422"
