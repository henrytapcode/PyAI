import hashlib
from typing import Any


def _canonical_repr(value: Any) -> str:
    if isinstance(value, dict):
        items = ", ".join(
            f"{k!r}: {_canonical_repr(value[k])}" for k in sorted(value)
        )
        return "{" + items + "}"
    if isinstance(value, list):
        return "[" + ", ".join(_canonical_repr(item) for item in value) + "]"
    return repr(value)


def make_key(model: str, messages: list[dict], **params) -> str:
    """Build a 64-char SHA-256 cache key using canonical sorted repr."""
    clean_msgs = [
        {
            **msg,
            "content": " ".join(msg["content"].strip().split())
            if isinstance(msg.get("content"), str)
            else msg.get("content"),
        }
        for msg in messages
    ]
    payload = {
        "model": model,
        "messages": clean_msgs,
        "params": params,
    }
    return hashlib.sha256(_canonical_repr(payload).encode("utf-8")).hexdigest()


class TTLCache:
    """In-memory TTL cache storing plain (value, expires_at) tuples."""

    def __init__(self, ttl: float) -> None:
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        self._entries: dict[str, tuple[Any, float]] = {}

    def set(self, key: str, value: Any, now: float) -> None:
        self._entries[key] = (value, now + self.ttl)

    def get(self, key: str, now: float) -> Any:
        item = self._entries.get(key)
        if item is None:
            self.misses += 1
            return None
        value, expires_at = item
        if now >= expires_at:
            del self._entries[key]
            self.misses += 1
            return None
        self.hits += 1
        return value

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def __len__(self) -> int:
        return len(self._entries)
