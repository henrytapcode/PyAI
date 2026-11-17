from collections import OrderedDict


class LRUCache:
    """In-memory LRU cache backed by OrderedDict with hit, miss, and eviction counters."""

    def __init__(self, maxsize: int) -> None:
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self.maxsize = maxsize
        self._data: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def peek(self, key: str):
        """Return cached value or None without changing recency or hit/miss counts."""
        return self._data.get(key)

    def get(self, key: str):
        """Return cached value and mark key as recent, or None on miss.

        Example: cache.get("missing") -> None
        """
        if key not in self._data:
            self.misses += 1
            return None
        self._data.move_to_end(key)
        self.hits += 1
        return self._data[key]

    def set(self, key: str, value) -> None:
        """Insert or update key and evict least recently used item if full."""
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)
            self.evictions += 1

    def __len__(self) -> int:
        return len(self._data)
