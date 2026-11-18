from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, ConfigDict, Field


class MessageRequest(BaseModel):
    """Validated JSON body for POST /sessions/{sid}/messages."""

    model_config = ConfigDict(str_strip_whitespace=True)
    question: str = Field(min_length=1)


def create_app(
    make_bot,
    clock,
    session_ttl: float = 600.0,
    max_sessions: int = 100,
) -> FastAPI:
    """Create a FastAPI session service wrapping per-session chatbot instances.

    Example:
        app = create_app(make_bot, clock, session_ttl=60.0, max_sessions=2)
        GET  /health               -> 200 {"status": "ok", "active_sessions": 0}
        POST /sessions             -> 201 {"session_id": "s1"}
        POST /sessions/s1/messages {"question": "What about express?"}
            -> 200 {"answer": "...", "sources": [...], "rewritten": "...", "turn": 1}
        GET  /sessions/s1          -> 200 {"session_id": "s1", "turns": [...]}
    """
    app = FastAPI()
    # TODO: raise ValueError if max_sessions < 1 or session_ttl <= 0
    # TODO: keep sessions dict and counter inside create_app (no module-level state)
    # TODO: at the start of every request, remove sessions with clock() - last_seen >= session_ttl
    # TODO: register GET /health -> {"status": "ok", "active_sessions": len(sessions)}
    # TODO: register POST /sessions (201) -> evict LRU (tie-break by created) if full,
    #       call make_bot() once, store {"bot", "turns", "last_seen", "created"},
    #       return {"session_id": sid}
    # TODO: register POST /sessions/{sid}/messages -> 404 if missing/expired, call bot.ask,
    #       record turn, refresh last_seen, return {"answer", "sources", "rewritten", "turn"}
    # TODO: register GET /sessions/{sid} -> 404 if missing/expired, refresh last_seen,
    #       return {"session_id": sid, "turns": [...]}
    return app
