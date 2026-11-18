# Manage isolated chat sessions with FakeClock TTL expiration and capacity eviction.
class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


class SessionStore:
    def __init__(self, clock: FakeClock, ttl: float = 60.0, max_sessions: int = 2) -> None:
        self.clock = clock
        self.ttl = ttl
        self.max_sessions = max_sessions
        self.sessions: dict[str, dict] = {}

    def _purge_expired(self) -> None:
        now = self.clock()
        expired = [sid for sid, item in self.sessions.items() if now - item["last_seen"] >= self.ttl]
        for sid in expired:
            del self.sessions[sid]

    def create(self, sid: str) -> None:
        self._purge_expired()
        if sid not in self.sessions and len(self.sessions) >= self.max_sessions:
            oldest = min(self.sessions, key=lambda k: self.sessions[k]["last_seen"])
            del self.sessions[oldest]
        self.sessions[sid] = {"history": [], "last_seen": self.clock()}

    def append_turn(self, sid: str, role: str, content: str) -> bool:
        self._purge_expired()
        item = self.sessions.get(sid)
        if item is None:
            return False
        item["history"].append({"role": role, "content": content})
        item["last_seen"] = self.clock()
        return True

    def snapshot(self) -> dict[str, int]:
        self._purge_expired()
        return {sid: len(item["history"]) for sid, item in self.sessions.items()}


clock = FakeClock(start=0.0)
store = SessionStore(clock=clock, ttl=60.0, max_sessions=2)

store.create("alice")
store.append_turn("alice", "user", "How long do refunds take?")
print("t=0  create alice:", store.snapshot())

clock.advance(20.0)
store.create("bob")
print("t=20 create bob  :", store.snapshot())

clock.advance(10.0)
store.append_turn("alice", "user", "What about opened software?")
print("t=30 touch alice :", store.snapshot())

clock.advance(10.0)
store.create("carol")
print("t=40 create carol:", store.snapshot())

clock.advance(50.0)
print("t=90 after ttl   :", store.snapshot())
print("t=90 alice ok?   :", store.append_turn("alice", "user", "Still there?"))
