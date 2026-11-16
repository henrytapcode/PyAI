Complete the `LRUCache` class in `starter.py` by replacing every `___` blank so it stores up to `maxsize` items, evicts the least recently used key, and tracks `hits` and `misses`. Fill in the blanks inside the methods and keep the existing method signatures.

**Example**

```python
cache = LRUCache(maxsize=2)
cache.set("a", 1)
cache.set("b", 2)
cache.get("a")   # 1 (moves "a" to most recently used)
cache.set("c", 3)  # evicts "b"
cache.get("b")   # None (cache miss)
```

**Rules**
- `get(key)` returns `None` and increments `self.misses` when `key` is missing; on a hit it marks `key` as most recently used, increments `self.hits`, and returns the stored value.
- `set(key, value)` stores or updates `key` as most recently used; if the cache size exceeds `self.maxsize`, it removes the least recently used entry (`last=False`).
- Updating an existing key with `set(key, new_value)` updates its value without increasing cache size or evicting another key.
