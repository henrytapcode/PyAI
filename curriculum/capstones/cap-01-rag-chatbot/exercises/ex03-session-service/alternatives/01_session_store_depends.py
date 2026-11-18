from collections import OrderedDict
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field


class MessageRequest(BaseModel):
    """Validated JSON body for POST /sessions/{sid}/messages."""

    model_config = ConfigDict(str_strip_whitespace=True)
    question: str = Field(min_length=1)


class SessionStore:
    """OrderedDict-backed TTL and O(1) LRU session store."""

    def __init__(self, make_bot, clock, session_ttl: float, max_sessions: int) -> None:
        if max_sessions < 1 or session_ttl <= 0:
            raise ValueError("max_sessions must be >= 1 and session_ttl must be > 0")
        self._make_bot = make_bot
        self._clock = clock
        self._ttl = session_ttl
        self._max_sessions = max_sessions
        self._counter = 0
        self._entries: OrderedDict[str, dict] = OrderedDict()

    def purge(self) -> float:
        """Delete all expired sessions and return the current clock timestamp."""
        now = self._clock()
        expired = [
            sid for sid, record in self._entries.items() if now - record["last_seen"] >= self._ttl
        ]
        for sid in expired:
            del self._entries[sid]
        return now

    def active_count(self) -> int:
        """Return active session count after purging expired entries."""
        self.purge()
        return len(self._entries)

    def create(self) -> str:
        """Create a new session, evicting the least recently used entry if full."""
        now = self.purge()
        if len(self._entries) >= self._max_sessions:
            self._entries.popitem(last=False)
        self._counter += 1
        sid = f"s{self._counter}"
        self._entries[sid] = {
            "bot": self._make_bot(),
            "turns": [],
            "last_seen": now,
            "created": self._counter,
        }
        return sid

    def touch(self, sid: str) -> dict:
        """Fetch an active session, refresh its recency, or raise 404."""
        now = self.purge()
        record = self._entries.get(sid)
        if record is None:
            raise HTTPException(status_code=404, detail="session not found")
        record["last_seen"] = now
        self._entries.move_to_end(sid)
        return record


def create_app(
    make_bot,
    clock,
    session_ttl: float = 600.0,
    max_sessions: int = 100,
) -> FastAPI:
    """Create a FastAPI session service using SessionStore and Depends injection."""
    store = SessionStore(make_bot, clock, session_ttl, max_sessions)
    app = FastAPI()

    def get_store() -> SessionStore:
        store.purge()
        return store

    def get_active_session(
        sid: str,
        active_store: Annotated[SessionStore, Depends(get_store)],
    ) -> dict:
        return active_store.touch(sid)

    @app.get("/health")
    def health(
        active_store: Annotated[SessionStore, Depends(get_store)],
    ) -> dict[str, object]:
        return {"status": "ok", "active_sessions": active_store.active_count()}

    @app.post("/sessions", status_code=201)
    def start_session(
        active_store: Annotated[SessionStore, Depends(get_store)],
    ) -> dict[str, str]:
        return {"session_id": active_store.create()}

    @app.post("/sessions/{sid}/messages")
    def post_message(
        body: MessageRequest,
        record: Annotated[dict, Depends(get_active_session)],
    ) -> dict[str, object]:
        reply = record["bot"].ask(body.question)
        record["turns"].append({"question": body.question, "answer": reply["answer"]})
        return {
            "answer": reply["answer"],
            "sources": reply["sources"],
            "rewritten": reply["rewritten"],
            "turn": len(record["turns"]),
        }

    @app.get("/sessions/{sid}")
    def get_session(
        sid: str,
        record: Annotated[dict, Depends(get_active_session)],
    ) -> dict[str, object]:
        return {"session_id": sid, "turns": [dict(turn) for turn in record["turns"]]}

    return app
