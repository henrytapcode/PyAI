Complete the in-memory notes FastAPI app by replacing every `___` blank with the right field name, decorator method, type hint, or HTTP status code.

**Example**

```text
GET  /notes       -> 200 []
POST /notes       -> 201 {"id": 1, "text": "ship v1"}   (body: {"text": "ship v1"})
GET  /notes/999   -> 404 {"detail": "note not found"}
GET  /notes/abc   -> 422
POST /notes       -> 422                                (body: {})
```

**Rules**
- Replace each `___` blank in `NoteCreate`, the route decorators, and `get_note`.
- Keep the existing `app` and `notes` names intact; tests reset `notes` via a fixture.
- Do not change the return dictionary shapes.
