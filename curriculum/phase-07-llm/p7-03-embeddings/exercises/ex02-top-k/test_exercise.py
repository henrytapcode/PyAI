from exercise import top_k
from pyai_llm import FakeLLM


class _SpyClient:
    def __init__(self, embed_dim: int = 256) -> None:
        self._inner = FakeLLM(embed_dim=embed_dim)
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        return self._inner.embed(texts)


def test_synonym_query_ranks_first():
    client = FakeLLM(embed_dim=256)
    docs = [
        "fast laptop repair",
        "cheap car rental",
        "book a doctor visit",
    ]
    result = top_k("affordable automobile", docs, client, k=2)
    assert result is not None, "top_k returned None: did you forget to return the list?"
    assert len(result) == 2
    assert result[0][0] == 1, f"expected synonym match at index 1 first, got {result}"
    assert result[0][1] > 0.7


def test_returns_at_most_k_and_handles_k_larger_than_docs():
    client = FakeLLM(embed_dim=256)
    docs = ["cheap car", "fast laptop", "full refund"]
    two = top_k("affordable car", docs, client, k=2)
    assert two is not None
    assert len(two) == 2
    many = top_k("affordable car", docs, client, k=10)
    assert many is not None
    assert len(many) == 3


def test_scores_are_sorted_descending():
    client = FakeLLM(embed_dim=256)
    docs = [
        "fast kitten",
        "cheap car",
        "cheap car repair",
        "doctor visit",
    ]
    result = top_k("affordable automobile", docs, client, k=4)
    assert result is not None
    scores = [score for _, score in result]
    assert scores == sorted(scores, reverse=True)


def test_tie_breaks_by_smaller_index():
    client = FakeLLM(embed_dim=256)
    docs = ["cheap car", "cheap car", "fast laptop", "cheap car"]
    result = top_k("affordable automobile", docs, client, k=3)
    assert result is not None
    assert [idx for idx, _ in result] == [0, 1, 3]
    assert result[0][1] == result[1][1] == result[2][1]


def test_min_score_filters_low_matches():
    client = FakeLLM(embed_dim=256)
    docs = ["cheap car rental", "fast laptop repair", "book a doctor"]
    filtered = top_k("affordable automobile", docs, client, k=3, min_score=0.5)
    assert filtered is not None
    assert [idx for idx, _ in filtered] == [0]

    none_match = top_k("spicy noodle soup", docs, client, k=3, min_score=0.3)
    assert none_match == []


def test_empty_docs_returns_empty_without_calling_embed():
    spy = _SpyClient()
    result = top_k("affordable automobile", [], spy, k=2)
    assert result == []
    assert spy.calls == [], "do not call client.embed when docs is empty"


def test_scores_are_python_float_rounded_to_three_decimals():
    client = FakeLLM(embed_dim=256)
    docs = ["cheap car rental", "fast laptop repair"]
    result = top_k("affordable automobile", docs, client, k=2)
    assert result is not None and len(result) > 0
    for idx, score in result:
        assert type(idx) is int
        assert type(score) is float, f"expected Python float, got {type(score).__name__}"
        assert score == round(score, 3)


def test_embeds_docs_in_single_batch_call():
    spy = _SpyClient()
    docs = ["cheap car", "fast laptop", "full refund", "happy kitten"]
    result = top_k("affordable automobile", docs, spy, k=2)
    assert result is not None
    assert 1 <= len(spy.calls) <= 2, (
        f"expected 1 combined call or 2 calls (docs + query), got {len(spy.calls)}"
    )
    if len(spy.calls) == 1:
        assert len(spy.calls[0]) == len(docs) + 1
    else:
        assert docs in spy.calls and ["affordable automobile"] in spy.calls
