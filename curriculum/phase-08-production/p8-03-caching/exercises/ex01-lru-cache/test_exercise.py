import exercise


def test_basic_set_and_get():
    cache = exercise.LRUCache(maxsize=2)
    cache.set("a", "alpha")
    cache.set("b", "beta")
    assert cache.get("a") == "alpha"
    assert cache.get("b") == "beta"
    assert cache.get("missing") is None


def test_evicts_least_recently_used_key():
    cache = exercise.LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.get("a") is None, "oldest untouched key 'a' should be evicted"
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_get_refreshes_key_recency():
    cache = exercise.LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    cache.set("c", 3)
    assert cache.get("b") is None, "reading 'a' should make 'b' the least recently used key"
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_counts_hits_and_misses():
    cache = exercise.LRUCache(maxsize=3)
    assert cache.get("x") is None
    cache.set("x", 10)
    assert cache.get("x") == 10
    assert cache.get("x") == 10
    assert cache.get("y") is None
    assert cache.hits == 2
    assert cache.misses == 2


def test_updating_existing_key_updates_value_without_growing():
    cache = exercise.LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("a", 99)
    assert len(cache) == 2
    assert cache.evictions == 0
    assert cache.get("a") == 99
    assert cache.get("b") == 2


def test_peek_reads_without_changing_recency_or_counters():
    cache = exercise.LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.peek("a") == 1
    assert cache.peek("missing") is None
    assert cache.hits == 0
    assert cache.misses == 0
    cache.set("c", 3)
    assert cache.get("a") is None, "peek('a') must not refresh 'a' recency"
    assert cache.get("b") == 2


def test_evictions_counts_each_capacity_eviction():
    cache = exercise.LRUCache(maxsize=2)
    assert cache.evictions == 0
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.evictions == 0
    cache.set("c", 3)
    assert cache.evictions == 1
    cache.set("d", 4)
    assert cache.evictions == 2
