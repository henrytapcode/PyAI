# In-memory notes API

**What it shows:** Combining `GET`, `POST` (`201 Created`), path parameters, and `HTTPException` (`404`) in a small in-memory notes service tested with `TestClient`.

**Step by step**
1. Lines 7–11 create the `FastAPI` app, an empty `notes` dictionary, and the `NoteCreate` Pydantic model requiring a non-empty `text` string.
2. Lines 14–22 define `GET /notes` to list stored notes sorted by ID and `GET /notes/{note_id}` to fetch one note or raise a `404` `HTTPException`.
3. Lines 25–29 define `POST /notes` with `status_code=201` to assign the next integer ID, save the note, and return the created record.
4. Lines 32–46 run six requests through `TestClient(app)` in order and print one compact line per response.

**Notice:** Calling `POST /notes` updates the in-memory `notes` dictionary immediately, so the second `GET /notes` sees both newly created records without a database.

**Try it yourself:** Add a `{"text": ""}` `POST /notes` step at the end of `steps` and watch FastAPI reject it with `422` without adding a third note.
