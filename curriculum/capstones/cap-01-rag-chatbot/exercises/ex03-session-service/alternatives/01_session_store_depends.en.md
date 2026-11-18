# SessionStore with OrderedDict LRU and FastAPI Depends

**How it works:** Instead of managing a plain dictionary and running `min(...)` inside closure functions, this alternative moves session lifecycle logic into a dedicated `SessionStore` class backed by `collections.OrderedDict`. Calling `move_to_end(sid)` on every access keeps entries ordered from least to most recently used so eviction is `popitem(last=False)` in O(1) time, while FastAPI's `Depends(get_active_session)` centralizes per-request expiration purging and `404` lookup across `{sid}` routes.

**When to choose it:** Pick this design when `max_sessions` grows large (avoiding an O(N) scan on every eviction), when you want to unit-test `SessionStore` separately from HTTP routing, or when multiple endpoints share the same session-validation dependency.
