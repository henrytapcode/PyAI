def make_key(model: str, messages: list[dict], **params) -> str | None:
    """Build a 64-char SHA-256 cache key for an LLM request.

    Example:
        make_key("mini", [{"role": "user", "content": " Hi  there "}], temperature=0.0)
        -> "e3b0c442..." (64 hex chars)
    """
    # TODO: normalize string content whitespace (strip + collapse spaces) without mutating messages,
    #       serialize with json.dumps(..., sort_keys=True), and return SHA-256 hexdigest()
    return None


class TTLCache:
    """In-memory cache with per-entry TTL using an injected timestamp `now`.

    Example:
        c = TTLCache(ttl=60.0)
        c.set("k", "ans", now=0.0)
        c.get("k", now=30.0)  # "ans"
        c.get("k", now=60.0)  # None
    """

    def __init__(self, ttl: float) -> None:
        # TODO: store ttl, initialize hits/misses counters and storage dict
        pass

    def set(self, key: str, value, now: float) -> None:
        """Store value with expiration timestamp now + ttl."""
        # TODO: save value and its expires_at timestamp
        return None

    def get(self, key: str, now: float):
        """Return value if present and not expired (now < expires_at), else None."""
        # TODO: handle missing key, delete if now >= expires_at, update hits/misses
        return None

    def hit_rate(self) -> float | None:
        """Return hits / (hits + misses), or 0.0 when no lookups happened yet."""
        # TODO: compute hit rate safely
        return None

    def __len__(self) -> int | None:
        """Return the number of entries currently stored in the cache."""
        # TODO: return entry count
        return None
