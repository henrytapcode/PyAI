Complete the `LRUCache` class in `starter.py` by replacing every `___` blank so it stores up to `maxsize` items, evicts the least recently used key, supports non-mutating `peek(key)` lookups, and tracks `hits`, `misses`, and `evictions`. Fill in the blanks inside the methods and keep the existing method signatures.

**Example**

```python
cache = LRUCache(maxsize=2)
cache.set("a", 1)
cache.set("b", 2)
cache.peek("a")  # 1 (does NOT change order or hits/misses)
cache.set("c", 3)  # evicts "a" (evictions == 1)
cache.get("a")   # None (cache miss)
cache.get("b")   # 2 (cache hit, moves "b" to most recently used)
```

**Rules**
- `peek(key)` returns the cached value or `None` without changing key order and without changing `self.hits` or `self.misses`.
- `get(key)` returns `None` and increments `self.misses` when `key` is missing; on a hit it marks `key` as most recently used, increments `self.hits`, and returns the stored value.
- `set(key, value)` stores or updates `key` as most recently used; if the cache size exceeds `self.maxsize`, it removes the least recently used entry and increments `self.evictions` by `1`.
- Updating an existing key with `set(key, new_value)` updates its value without increasing cache size, evicting another key, or incrementing `self.evictions`.
