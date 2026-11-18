# Isolated session store with FakeClock TTL and eviction

**What it shows:** Storing per-session chat histories in a bounded dictionary where stale sessions expire via `FakeClock` TTL and full capacity evicts the least recently used session.

**Step by step**
1. Lines 2–10 define the standard `FakeClock` callable for deterministic time advances.
2. Lines 13–44 define `SessionStore` tracking `{"history", "last_seen"}` per `session_id`, purging expired entries on access and evicting the oldest `last_seen` when at `max_sessions=2`.
3. Lines 47–58 create `"alice"` at `t=0`, create `"bob"` at `t=20`, and touch `"alice"` at `t=30`.
4. Lines 60–66 create `"carol"` at `t=40` (evicting `"bob"` instead of `"alice"`) and then advance to `t=90` so `"alice"` expires while `"carol"` stays active.

**Notice:** Touching `"alice"` at `t=30` updated her `last_seen` timestamp, so when `"carol"` arrived at `t=40`, `"bob"` (`last_seen=20`) was evicted instead of `"alice"`.

**Try it yourself:** Remove the `append_turn("alice", ...)` line at `t=30` and re-run to verify that `"alice"` (`last_seen=0`) gets evicted instead of `"bob"`.
