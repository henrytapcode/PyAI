import pytest
from exercise import MiniStore
from pyai_llm import FakeLLM


class _SpyClient:
    def __init__(self, embed_dim: int = 256) -> None:
        self._inner = FakeLLM(embed_dim=embed_dim)
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        return self._inner.embed(texts)


def test_synonym_query_ranks_first():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["c1", "c2", "c3"],
        ["fast laptop repair", "cheap car rental", "book a doctor visit"],
    )
    hits = store.search("affordable automobile", k=2)
    assert hits is not None, "search returned None: did you forget to return the list?"
    assert len(hits) == 2
    assert hits[0][0] == "c2", f"expected synonym match 'c2' first, got {hits}"
    assert type(hits[0][1]) is float
    assert hits[0][1] == round(hits[0][1], 3)


def test_respects_k_and_tie_breaks_by_insertion_order():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["c1", "c2", "c3", "c4"],
        ["cheap car", "fast laptop", "cheap car", "cheap car"],
    )
    top2 = store.search("affordable automobile", k=2)
    assert top2 == [("c1", 1.0), ("c3", 1.0)]
    all_hits = store.search("affordable automobile", k=10)
    assert [cid for cid, _ in all_hits] == ["c1", "c3", "c4", "c2"]


def test_pre_filter_returns_full_k_even_when_other_docs_score_higher():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["d1", "d2", "d3", "d4", "d5"],
        [
            "Full refund for broken laptop.",
            "Fast money back for notebook.",
            "Hoan tien refund cho laptop.",
            "Bao hanh computer trong 7 ngay.",
            "Thue xe cheap car theo ngay.",
        ],
        [
            {"lang": "en"},
            {"lang": "en"},
            {"lang": "vi"},
            {"lang": "vi"},
            {"lang": "vi"},
        ],
    )
    hits = store.search("money back for laptop", k=2, where={"lang": "vi"})
    assert hits is not None
    assert [cid for cid, _ in hits] == ["d3", "d4"]


def test_filter_with_no_match_returns_empty():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(["c1"], ["cheap car rental"], [{"lang": "en"}])
    assert store.search("cheap car", k=2, where={"lang": "fr"}) == []


def test_empty_store_returns_empty():
    store = MiniStore(FakeLLM(embed_dim=256))
    assert store.search("cheap car", k=3) == []
    assert len(store) == 0


def test_same_batch_duplicate_id_raises_value_error_without_mutating():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(["c1"], ["Full refund"])
    with pytest.raises(ValueError):
        store.add(["c3", "c3"], ["Cheap car", "Fast laptop"])
    assert len(store) == 1


def test_upsert_replaces_existing_record_and_preserves_length():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["c1", "c2"],
        ["cheap car rental", "fast laptop repair"],
        [{"lang": "en"}, {"lang": "en"}],
    )
    store.add(
        ["c1", "c3"],
        ["book a doctor visit", "cheap car rental"],
        [{"lang": "vi"}, {"lang": "fr"}],
    )
    assert len(store) == 3
    car_hits = store.search("affordable automobile", k=3)
    assert car_hits is not None and car_hits[0][0] == "c3"
    doc_hits = store.search("doctor appointment", k=1, where={"lang": "vi"})
    assert doc_hits is not None and doc_hits[0][0] == "c1"


def test_where_list_filter_and_missing_key():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["d1", "d2", "d3", "d4"],
        ["cheap car rental", "affordable car", "cheap car", "cheap car"],
        [{"lang": "en"}, {"lang": "vi"}, {"lang": "fr"}, {}],
    )
    hits = store.search("affordable automobile", k=5, where={"lang": ["en", "vi"]})
    assert hits is not None
    assert sorted(cid for cid, _ in hits) == ["d1", "d2"]
    assert store.search("cheap car", k=5, where={"lang": ["de", "es"]}) == []
    assert store.search("cheap car", k=5, where={"lang": [None]}) == []


def test_delete_removes_record_and_keeps_alignment():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(
        ["c1", "c2", "c3"],
        ["Full refund for broken laptop.", "Fast money back for notebook.", "Cheap car rental."],
    )
    store.delete("c2")
    assert len(store) == 2
    refund_hits = store.search("money back for laptop", k=3)
    assert [cid for cid, _ in refund_hits] == ["c1", "c3"]
    car_hits = store.search("affordable automobile", k=1)
    assert car_hits is not None and car_hits[0][0] == "c3"


def test_delete_missing_id_raises_key_error():
    store = MiniStore(FakeLLM(embed_dim=256))
    store.add(["c1"], ["Full refund"])
    with pytest.raises(KeyError):
        store.delete("missing")


def test_add_embeds_batch_in_single_call():
    spy = _SpyClient()
    store = MiniStore(spy)
    store.add(["c1", "c2", "c3"], ["cheap car", "fast laptop", "full refund"])
    assert len(spy.calls) == 1
    assert spy.calls[0] == ["cheap car", "fast laptop", "full refund"]
    store.search("affordable automobile", k=1)
    assert len(spy.calls) == 2
