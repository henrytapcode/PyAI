Implement a deterministic `make_key(model, messages, **params)` function and a `TTLCache` class in `starter.py`. Write your code inside the function and class methods and `return` the results.

**Example**

```python
msgs = [{"role": "system", "content": "Be concise."}, {"role": "user", "content": "  Hi   there "}]
k1 = make_key("mini", msgs, temperature=0.0, max_tokens=50)
k2 = make_key("mini", msgs, max_tokens=50, temperature=0.0)
k1 == k2  # True (64-char SHA-256 hex digest)

cache = TTLCache(ttl=30.0)
cache.set(k1, "Hello!", now=10.0)
cache.get(k1, now=39.9)  # "Hello!" (hit)
cache.get(k1, now=40.0)  # None (expired and deleted)
cache.hit_rate()         # 0.5
```

**Rules**
- `make_key(model, messages, **params)` strips leading/trailing whitespace and collapses internal whitespace runs in each message's string `content` without mutating `messages`, serializes the payload with `json.dumps(..., sort_keys=True)`, and returns the 64-character SHA-256 `hexdigest()`.
- Reordering keyword arguments in `**params` must yield the same key; changing `model`, `system` prompt, or `temperature` must yield a different key.
- `TTLCache(ttl)` accepts `now: float` in `set(key, value, now)` and `get(key, now)`: `get` returns `None` when missing or expired (`now >= expires_at`), deletes expired entries from storage, and updates `self.hits` and `self.misses`.
- `hit_rate()` returns `hits / (hits + misses)` as a `float`, or `0.0` if no lookups have occurred; `__len__()` returns the number of currently stored entries.
