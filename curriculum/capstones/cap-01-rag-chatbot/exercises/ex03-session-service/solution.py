from fastapi import FastAPI, HTTPException
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
    """Build an isolated FastAPI chat service with per-session bots, TTL, and LRU eviction."""
    if max_sessions < 1 or session_ttl <= 0:
        raise ValueError("max_sessions must be >= 1 and session_ttl must be > 0")

    app = FastAPI()
    sessions: dict[str, dict] = {}
    seq = 0

    def evict_expired(now: float) -> None:
        stale = [
            key
            for key, record in sessions.items()
            if now - record["last_seen"] >= session_ttl
        ]
        for key in stale:
            del sessions[key]

    def require_session(sid: str, now: float) -> dict:
        evict_expired(now)
        record = sessions.get(sid)
        if record is None:
            raise HTTPException(status_code=404, detail="session not found")
        record["last_seen"] = now
        return record

    @app.get("/health")
    def health() -> dict[str, object]:
        evict_expired(clock())
        return {"status": "ok", "active_sessions": len(sessions)}

    @app.post("/sessions", status_code=201)
    def start_session() -> dict[str, str]:
        nonlocal seq
        now = clock()
        evict_expired(now)
        if len(sessions) >= max_sessions:
            victim = min(
                sessions,
                key=lambda key: (sessions[key]["last_seen"], sessions[key]["created"]),
            )
            del sessions[victim]
        seq += 1
        sid = f"s{seq}"
        sessions[sid] = {
            "bot": make_bot(),
            "turns": [],
            "last_seen": now,
            "created": seq,
        }
        return {"session_id": sid}

    @app.post("/sessions/{sid}/messages")
    def post_message(sid: str, body: MessageRequest) -> dict[str, object]:
        record = require_session(sid, clock())
        reply = record["bot"].ask(body.question)
        record["turns"].append({"question": body.question, "answer": reply["answer"]})
        return {
            "answer": reply["answer"],
            "sources": reply["sources"],
            "rewritten": reply["rewritten"],
            "turn": len(record["turns"]),
        }

    @app.get("/sessions/{sid}")
    def get_session(sid: str) -> dict[str, object]:
        record = require_session(sid, clock())
        return {
            "session_id": sid,
            "turns": [dict(turn) for turn in record["turns"]],
        }

    return app
