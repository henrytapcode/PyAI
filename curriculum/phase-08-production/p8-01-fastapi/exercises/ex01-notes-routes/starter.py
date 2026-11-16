from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
notes: dict[int, str] = {}


class NoteCreate(BaseModel):
    # TODO: name the required note text field to match body.text below
    ___: str = Field(min_length=1, max_length=100)


# TODO: fill in the HTTP method for listing all notes
@app.___("/notes")
def list_notes() -> list[dict[str, object]]:
    return [{"id": nid, "text": text} for nid, text in sorted(notes.items())]


# TODO: fill in the HTTP status code returned when a note is created
@app.post("/notes", status_code=___)
def create_note(body: NoteCreate) -> dict[str, object]:
    note_id = len(notes) + 1
    notes[note_id] = body.text
    return {"id": note_id, "text": body.text}


# TODO: fill in the path parameter type and the 404 status code
@app.get("/notes/{note_id}")
def get_note(note_id: ___) -> dict[str, object]:
    if note_id not in notes:
        raise HTTPException(status_code=___, detail="note not found")
    return {"id": note_id, "text": notes[note_id]}
