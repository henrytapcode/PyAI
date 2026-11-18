Build the FastAPI session service factory `create_app(make_bot, clock, session_ttl=600.0, max_sessions=100) -> FastAPI`. While the lesson §6 snippet only keeps raw history dicts in pure Python, this exercise adds the FastAPI routes and HTTP status codes, a dedicated bot per session, expiration cleanup on every request, `404` responses for missing or expired sessions, `422` validation for blank questions, and 1-based turn counting. Write your code inside `create_app` (plus Pydantic models or helpers) and return the configured `FastAPI` instance. In production or with your `ex01` solution, wire the real bot by passing `lambda: ChatBot(DOCS, client)` as `make_bot`.

**Example**

```python
from fastapi.testclient import TestClient

client = TestClient(create_app(make_bot, clock, session_ttl=60.0, max_sessions=2))

client.get("/health").json()
# -> {"status": "ok", "active_sessions": 0}

s1 = client.post("/sessions")
# status_code == 201, s1.json() -> {"session_id": "s1"}

r1 = client.post("/sessions/s1/messages", json={"question": "How much does shipping cost?"})
# status_code == 200, r1.json() -> {"answer": "...", "sources": [...], "rewritten": "...", "turn": 1}

client.get("/sessions/s1").json()
# -> {"session_id": "s1", "turns": [{"question": "How much does shipping cost?", "answer": "..."}]}

clock.advance(60.0)
client.get("/sessions/s1").status_code
# -> 404
```

**Rules**

- Signature: `create_app(make_bot, clock, session_ttl: float = 600.0, max_sessions: int = 100) -> FastAPI`. Raise `ValueError` immediately if `max_sessions < 1` or `session_ttl <= 0`.
- Keep all session state inside `create_app`'s closure so separate apps never share sessions (no module-level mutable state).
- Store each session as `{"bot": ..., "turns": list[{"question", "answer"}], "last_seen": float, "created": int}` with deterministic IDs `"s1"`, `"s2"`, … from the app's counter.
- **Expiration:** at the start of **every** request, remove all sessions where `clock() - last_seen >= session_ttl`.
- `GET /health` returns `200` with `{"status": "ok", "active_sessions": n}`.
- `POST /sessions` returns `201` with `{"session_id": "sN"}` and calls `make_bot()` **once** for the new session. If after purging expired sessions `len(sessions) >= max_sessions`, evict the session with the smallest `last_seen` (breaking ties by smallest `created`).
- `POST /sessions/{sid}/messages` validates body `{"question": str}` with Pydantic (`min_length=1` after stripping whitespace, so empty or whitespace-only questions return `422`), calls the session's `bot.ask(question)` (returning `{"answer", "sources", "rewritten"}`), appends `{"question", "answer"}` to `turns`, updates `last_seen`, and returns `200` with `{"answer", "sources", "rewritten", "turn": n}` (`n` starting at `1`).
- `GET /sessions/{sid}` updates `last_seen` and returns `200` with `{"session_id": sid, "turns": [...]}`.
- Both `{sid}` routes return `404` with `{"detail": "session not found"}` when `sid` does not exist or has expired.
