from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
notes: dict[int, str] = {}


class NoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=100)


def _note_payload(note_id: int) -> dict[str, object]:
    return {"id": note_id, "text": notes[note_id]}


@app.get("/notes")
def list_notes() -> list[dict[str, object]]:
    return [_note_payload(nid) for nid in sorted(notes)]


@app.post("/notes", status_code=201)
def create_note(body: NoteCreate) -> dict[str, object]:
    note_id = len(notes) + 1
    notes[note_id] = body.text
    return _note_payload(note_id)


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> dict[str, object]:
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="note not found")
    return _note_payload(note_id)
