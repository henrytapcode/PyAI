import pytest

import exercise


def test_make_key_returns_64_char_hex():
    key = exercise.make_key(
        "fake-mini",
        [{"role": "user", "content": "What is RAG?"}],
        temperature=0.0,
    )
    assert isinstance(key, str)
    assert len(key) == 64
    assert all(ch in "0123456789abcdef" for ch in key)


def test_make_key_is_identical_when_params_reordered():
    msgs = [{"role": "user", "content": "How do I reset my password?"}]
    k1 = exercise.make_key("fake-mini", msgs, temperature=0.0, max_tokens=100, top_p=1.0)
    k2 = exercise.make_key("fake-mini", msgs, top_p=1.0, max_tokens=100, temperature=0.0)
    assert isinstance(k1, str) and k1 == k2


def test_make_key_normalizes_whitespace_without_mutating_input():
    msgs_raw = [{"role": "user", "content": "  Reset   my\tpassword?  "}]
    msgs_clean = [{"role": "user", "content": "Reset my password?"}]
    k_raw = exercise.make_key("fake-mini", msgs_raw, temperature=0.0)
    k_clean = exercise.make_key("fake-mini", msgs_clean, temperature=0.0)
    assert isinstance(k_raw, str) and k_raw == k_clean
    assert msgs_raw[0]["content"] == "  Reset   my\tpassword?  "


@pytest.mark.parametrize(
    "other_model,other_messages,other_temp",
    [
        (
            "fake-large",
            [
                {"role": "system", "content": "Be concise."},
                {"role": "user", "content": "What is RAG?"},
            ],
            0.0,
        ),
        (
            "fake-mini",
            [
                {"role": "system", "content": "Be a pirate."},
                {"role": "user", "content": "What is RAG?"},
            ],
            0.0,
        ),
        (
            "fake-mini",
            [
                {"role": "system", "content": "Be concise."},
                {"role": "user", "content": "What is RAG?"},
            ],
            0.5,
        ),
    ],
)
def test_make_key_changes_when_model_system_or_temperature_changes(
    other_model, other_messages, other_temp
):
    base = exercise.make_key(
        "fake-mini",
        [
            {"role": "system", "content": "Be concise."},
            {"role": "user", "content": "What is RAG?"},
        ],
        temperature=0.0,
    )
    changed = exercise.make_key(other_model, other_messages, temperature=other_temp)
    assert changed != base


def test_ttl_cache_hits_before_expiry_and_misses_at_expiry():
    cache = exercise.TTLCache(ttl=60.0)
    cache.set("k1", "cached reply", now=10.0)
    assert cache.get("k1", now=69.9) == "cached reply"
    assert cache.get("k1", now=70.0) is None, "entry should expire when now == expires_at"


def test_ttl_cache_deletes_expired_entry():
    cache = exercise.TTLCache(ttl=30.0)
    cache.set("k1", "v1", now=0.0)
    assert len(cache) == 1
    assert cache.get("k1", now=30.0) is None
    assert len(cache) == 0, "expired entry should be removed from storage"


def test_ttl_cache_computes_hit_rate():
    cache = exercise.TTLCache(ttl=50.0)
    cache.set("k1", "v1", now=0.0)
    assert cache.get("k1", now=10.0) == "v1"
    assert cache.get("k1", now=20.0) == "v1"
    assert cache.get("k1", now=30.0) == "v1"
    assert cache.get("missing", now=35.0) is None
    assert cache.hits == 3
    assert cache.misses == 1
    assert cache.hit_rate() == pytest.approx(0.75)


def test_ttl_cache_empty_hit_rate_is_zero():
    cache = exercise.TTLCache(ttl=50.0)
    assert cache.hit_rate() == 0.0
