from exercise import answer_with_sources
from pyai_llm import FakeLLM

CHUNKS = [
    {"text": "Refunds are issued within 30 days of purchase.", "source": "refunds.md"},
    {"text": "Standard shipping delivers orders in five business days.", "source": "shipping.md"},
    {"text": "Hardware warranty covers factory defects for 12 months.", "source": "warranty.md"},
]


class _SpyClient:
    def __init__(self, script=None, embed_dim: int = 256) -> None:
        self._inner = FakeLLM(embed_dim=embed_dim, script=script)
        self.embed_calls: list[list[str]] = []
        self.chat_calls: list[list[dict]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls.append(list(texts))
        return self._inner.embed(texts)

    def chat(self, messages: list[dict], **kwargs):
        self.chat_calls.append([dict(m) for m in messages])
        return self._inner.chat(messages, **kwargs)


def test_answers_question_and_cites_correct_source():
    client = FakeLLM(embed_dim=256)
    res = answer_with_sources("How many days do refunds take?", CHUNKS, client)
    assert res is not None, "returned None: implement answer_with_sources"
    assert "30 days" in res["answer"]
    assert res["sources"] == ["refunds.md"]


def test_out_of_scope_skips_chat_and_returns_idk():
    spy = _SpyClient()
    res = answer_with_sources("Do you offer student discounts?", CHUNKS, spy, min_score=0.2)
    assert res == {"answer": "I don't know.", "sources": []}
    assert len(spy.chat_calls) == 0, "do not call chat when top score < min_score"


def test_empty_chunks_returns_idk_without_calling_chat():
    spy = _SpyClient()
    res = answer_with_sources("How many days do refunds take?", [], spy)
    assert res == {"answer": "I don't know.", "sources": []}
    assert len(spy.chat_calls) == 0


def test_system_message_uses_fixed_context_format_with_k_chunks():
    spy = _SpyClient()
    res = answer_with_sources("How many days do refunds take?", CHUNKS, spy, k=2)
    assert res is not None
    assert len(spy.chat_calls) == 1
    sent = spy.chat_calls[0]
    system_msgs = [m["content"] for m in sent if m["role"] == "system"]
    assert len(system_msgs) == 1
    lines = system_msgs[0].splitlines()
    assert "Context:" in lines
    ctx_lines = lines[lines.index("Context:") + 1 :]
    numbered = [ln for ln in ctx_lines if ln.startswith("[")]
    assert len(numbered) == 2
    assert numbered[0].startswith("[1] ")
    assert numbered[1].startswith("[2] ")


def test_ignores_out_of_range_citation():
    spy = _SpyClient(script=["See details [5]."])
    res = answer_with_sources("How many days do refunds take?", CHUNKS, spy, k=2)
    assert res is not None
    assert res["sources"] == []


def test_preserves_citation_order_and_deduplicates():
    spy = _SpyClient(script=["First [2], then [1], again [2]."])
    res = answer_with_sources("How many days do refunds take?", CHUNKS, spy, k=2)
    assert res is not None
    assert len(spy.chat_calls) == 1
    lines = [m["content"] for m in spy.chat_calls[0] if m["role"] == "system"][0].splitlines()
    ctx = [ln for ln in lines[lines.index("Context:") + 1 :] if ln.startswith("[")]
    src_by_text = {c["text"]: c["source"] for c in CHUNKS}
    expected = [src_by_text[ctx[1][4:]], src_by_text[ctx[0][4:]]]
    assert res["sources"] == expected


def test_embeds_chunks_and_question_in_at_most_two_calls():
    spy = _SpyClient()
    res = answer_with_sources("How many days do refunds take?", CHUNKS, spy, k=2)
    assert res is not None
    assert len(spy.embed_calls) in (1, 2)
    if len(spy.embed_calls) == 2:
        assert spy.embed_calls[0] == [c["text"] for c in CHUNKS]
        assert spy.embed_calls[1] == ["How many days do refunds take?"]
    else:
        expected_texts = [c["text"] for c in CHUNKS] + ["How many days do refunds take?"]
        assert spy.embed_calls[0] == expected_texts


def test_return_shape_and_types():
    res = answer_with_sources("How many days do refunds take?", CHUNKS, FakeLLM(embed_dim=256))
    assert isinstance(res, dict)
    assert set(res) == {"answer", "sources"}
    assert isinstance(res["answer"], str)
    assert isinstance(res["sources"], list)
