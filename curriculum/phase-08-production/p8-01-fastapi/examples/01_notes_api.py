# In-memory notes API exercised through FastAPI TestClient.

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()
notes: dict[int, str] = {}


class NoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=100)


@app.get("/notes")
def list_notes() -> list[dict[str, object]]:
    return [{"id": nid, "text": text} for nid, text in sorted(notes.items())]


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> dict[str, object]:
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": note_id, "text": notes[note_id]}


@app.post("/notes", status_code=201)
def create_note(body: NoteCreate) -> dict[str, object]:
    note_id = len(notes) + 1
    notes[note_id] = body.text
    return {"id": note_id, "text": body.text}


client = TestClient(app)
steps = [
    ("GET", "/notes", None),
    ("POST", "/notes", {"text": "log bug"}),
    ("POST", "/notes", {"text": "ship"}),
    ("GET", "/notes", None),
    ("GET", "/notes/2", None),
    ("GET", "/notes/99", None),
]

for method, path, payload in steps:
    if method == "GET":
        r = client.get(path)
    else:
        r = client.post(path, json=payload)
    print(f"{method:4s} {path:9s} {r.status_code} {r.json()}")
