import pytest
from exercise import build_index, retrieve
from pyai_llm import FakeLLM


class SpyClient:
    def __init__(self, embed_dim: int = 256) -> None:
        self._inner = FakeLLM(embed_dim=embed_dim)
        self.embed_calls = 0
        self.batch_sizes: list[int] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls += 1
        self.batch_sizes.append(len(texts))
        return self._inner.embed(texts)


@pytest.fixture
def sample_docs() -> list[dict]:
    return [
        {
            "source": "refunds.md",
            "text": "Refunds are issued within 30 days. Keep your original receipt!",
        },
        {
            "source": "shipping.md",
            "text": (
                "Standard shipping takes 5 business days across the country. "
                "Express takes 1 day."
            ),
        },
    ]


def test_build_index_sentence_mode_chunks_and_ids(sample_docs):
    client = FakeLLM(embed_dim=256)
    index = build_index(sample_docs, client, mode="sentence")
    assert isinstance(index, dict)
    assert [c["id"] for c in index["chunks"]] == [
        "refunds.md#0",
        "refunds.md#1",
        "shipping.md#0",
        "shipping.md#1",
    ]
    assert [c["source"] for c in index["chunks"]] == [
        "refunds.md",
        "refunds.md",
        "shipping.md",
        "shipping.md",
    ]


def test_build_index_words_mode_chunks_and_ids(sample_docs):
    client = FakeLLM(embed_dim=256)
    index = build_index(sample_docs, client, mode="words", size=5, overlap=2)
    assert isinstance(index, dict)
    refund_chunks = [c for c in index["chunks"] if c["source"] == "refunds.md"]
    assert [c["id"] for c in refund_chunks] == ["refunds.md#0", "refunds.md#1", "refunds.md#2"]
    assert refund_chunks[0]["text"] == "Refunds are issued within 30"
    assert refund_chunks[1]["text"] == "within 30 days. Keep your"


@pytest.mark.parametrize("bad_mode", ["char", "", "paragraph"])
def test_build_index_invalid_mode_raises_value_error(sample_docs, bad_mode):
    client = FakeLLM(embed_dim=256)
    with pytest.raises(ValueError):
        build_index(sample_docs, client, mode=bad_mode)


def test_build_index_skips_empty_documents():
    docs = [
        {"source": "empty.md", "text": "   "},
        {"source": "warranty.md", "text": "Warranty covers 12 months. Water damage excluded."},
    ]
    client = FakeLLM(embed_dim=256)
    index = build_index(docs, client, mode="sentence")
    assert isinstance(index, dict)
    assert [c["id"] for c in index["chunks"]] == ["warranty.md#0", "warranty.md#1"]


def test_build_index_calls_embed_once_with_all_chunks(sample_docs):
    spy = SpyClient(embed_dim=256)
    index = build_index(sample_docs, spy, mode="sentence")
    assert isinstance(index, dict)
    assert spy.embed_calls == 1, "build_index should embed all chunks in one batch call"
    assert spy.batch_sizes == [4]


def test_build_index_does_not_mutate_docs(sample_docs):
    snapshot = [dict(d) for d in sample_docs]
    index = build_index(sample_docs, FakeLLM(embed_dim=256), mode="sentence")
    assert isinstance(index, dict) and len(index["chunks"]) == 4
    assert sample_docs == snapshot


def test_retrieve_returns_expected_top_source_and_rounded_score(sample_docs):
    client = FakeLLM(embed_dim=256)
    index = build_index(sample_docs, client, mode="sentence")
    hits = retrieve(index, "How are refunds issued within 30 days?", client, k=2, min_score=0.2)
    assert isinstance(hits, list) and len(hits) >= 1
    assert hits[0]["source"] == "refunds.md"
    assert hits[0]["id"] == "refunds.md#0"
    assert set(hits[0].keys()) == {"id", "source", "text", "score"}
    assert hits[0]["score"] == round(hits[0]["score"], 3)


def test_retrieve_filters_everything_below_high_min_score(sample_docs):
    client = FakeLLM(embed_dim=256)
    index = build_index(sample_docs, client, mode="sentence")
    hits = retrieve(index, "How many days do refunds take?", client, k=2, min_score=0.99)
    assert hits == []


def test_retrieve_handles_k_larger_than_chunk_count(sample_docs):
    client = FakeLLM(embed_dim=256)
    index = build_index(sample_docs, client, mode="sentence")
    hits = retrieve(index, "shipping days refunds", client, k=50, min_score=0.0)
    assert isinstance(hits, list)
    assert len(hits) == 4


def test_retrieve_handles_empty_index_and_zero_k(sample_docs):
    client = FakeLLM(embed_dim=256)
    empty_index = build_index([], client, mode="sentence")
    assert retrieve(empty_index, "refunds?", client, k=2) == []
    non_empty = build_index(sample_docs, client, mode="sentence")
    assert retrieve(non_empty, "refunds?", client, k=0) == []
