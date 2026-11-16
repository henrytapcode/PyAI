from dataclasses import dataclass
import hashlib
import json
from typing import Any


def make_key(model: str, messages: list[dict], **params) -> str:
    """Build a 64-char SHA-256 cache key for an LLM request."""
    clean_msgs: list[dict] = []
    for msg in messages:
        copied = dict(msg)
        if isinstance(copied.get("content"), str):
            copied["content"] = " ".join(copied["content"].strip().split())
        clean_msgs.append(copied)

    payload = {
        "model": model,
        "messages": clean_msgs,
        "params": params,
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass
class _Entry:
    value: Any
    expires_at: float


class TTLCache:
    """In-memory cache with per-entry TTL using an injected timestamp `now`."""

    def __init__(self, ttl: float) -> None:
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        self._entries: dict[str, _Entry] = {}

    def set(self, key: str, value: Any, now: float) -> None:
        """Store value with expiration timestamp now + ttl."""
        self._entries[key] = _Entry(value=value, expires_at=now + self.ttl)

    def get(self, key: str, now: float) -> Any:
        """Return value if present and not expired (now < expires_at), else None."""
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        if now >= entry.expires_at:
            del self._entries[key]
            self.misses += 1
            return None
        self.hits += 1
        return entry.value

    def hit_rate(self) -> float:
        """Return hits / (hits + misses), or 0.0 when no lookups happened yet."""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total

    def __len__(self) -> int:
        """Return the number of entries currently stored in the cache."""
        return len(self._entries)
