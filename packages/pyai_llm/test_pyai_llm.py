"""Tests for the deterministic fake LLM client ``pyai_llm``."""

from __future__ import annotations

import json
import math

import pytest

from pyai_llm import (
    ChatResponse,
    FakeLLM,
    RateLimitError,
    ToolCall,
    Usage,
    __version__,
    cosine,
    count_tokens,
)


def test_version_and_exports() -> None:
    assert __version__ == "0.1.0"
    assert isinstance(Usage(1, 2, 3), Usage)
    assert isinstance(ChatResponse(content="ok"), ChatResponse)


def test_count_tokens_words_and_punctuation() -> None:
    assert count_tokens("") == 0
    assert count_tokens("Hello, world!") == 4
    assert count_tokens("one two three") == 3


def test_usage_counts_match_formula() -> None:
    client = FakeLLM()
    messages = [
        {"role": "system", "content": "Be concise."},
        {"role": "user", "content": "Say hi!"},
    ]
    resp = client.chat(messages)
    expected_prompt = (count_tokens("Be concise.") + 4) + (count_tokens("Say hi!") + 4)
    expected_completion = count_tokens(resp.content or "")
    assert resp.usage.prompt_tokens == expected_prompt
    assert resp.usage.completion_tokens == expected_completion
    assert resp.usage.total_tokens == expected_prompt + expected_completion


def test_max_tokens_truncates_and_sets_finish_reason_length() -> None:
    client = FakeLLM(script=["One two three four five six."])
    resp = client.chat([{"role": "user", "content": "Count"}], max_tokens=3)
    assert resp.finish_reason == "length"
    assert count_tokens(resp.content or "") == 3
    assert resp.content == "One two three"


def test_invalid_messages_raise_value_error() -> None:
    client = FakeLLM()
    with pytest.raises(ValueError, match="non-empty"):
        client.chat([])
    with pytest.raises(ValueError, match="invalid role"):
        client.chat([{"role": "developer", "content": "hi"}])
    with pytest.raises(ValueError, match="content"):
        client.chat([{"role": "user"}])
    with pytest.raises(ValueError, match="string"):
        client.chat([{"role": "user", "content": None}])  # type: ignore[list-item]


def test_fail_times_raises_rate_limit_then_succeeds() -> None:
    client = FakeLLM(fail_times=2, script=["recovered"])
    msg = [{"role": "user", "content": "hello"}]
    with pytest.raises(RateLimitError, match="rate limit"):
        client.chat(msg)
    with pytest.raises(RateLimitError, match="rate limit"):
        client.embed(["hello"])
    resp = client.chat(msg)
    assert resp.content == "recovered"


def test_script_replies_and_exhaustion_raises_index_error() -> None:
    client = FakeLLM(script=["first", "second"])
    msg = [{"role": "user", "content": "hi"}]
    assert client.chat(msg).content == "first"
    assert client.chat(msg).content == "second"
    with pytest.raises(IndexError, match="script exhausted after 2 replies"):
        client.chat(msg)


def test_script_overrides_tools_and_tool_results() -> None:
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        }
    ]
    client = FakeLLM(script=["script wins"])
    resp = client.chat(
        [{"role": "user", "content": "What is the weather in Tokyo?"}],
        tools=tools,
    )
    assert resp.content == "script wins"
    assert resp.tool_calls == []
    assert resp.finish_reason == "stop"


def test_script_can_emit_tool_calls_with_incrementing_ids() -> None:
    client = FakeLLM(
        script=[
            {"tool_calls": [{"name": "search", "arguments": {"q": "python"}}]},
            {"tool_calls": [{"name": "fetch", "arguments": {"id": 1}}]},
        ]
    )
    msg = [{"role": "user", "content": "run"}]
    r1 = client.chat(msg)
    r2 = client.chat(msg)
    assert r1.content is None
    assert r1.finish_reason == "tool_calls"
    assert r1.tool_calls == [ToolCall(id="call_1", name="search", arguments={"q": "python"})]
    assert r2.tool_calls == [ToolCall(id="call_2", name="fetch", arguments={"id": 1})]


def test_tool_result_takes_priority_over_new_tool_selection() -> None:
    tools = [
        {
            "name": "get_weather",
            "description": "Get weather temperature forecast",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        }
    ]
    client = FakeLLM()
    messages = [
        {"role": "user", "content": "What is the weather forecast for Paris?"},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [ToolCall(id="call_1", name="get_weather", arguments={"city": "Paris"})],
        },
        {"role": "tool", "tool_call_id": "call_1", "name": "get_weather", "content": "22C sunny"},
    ]
    resp = client.chat(messages, tools=tools)
    assert resp.finish_reason == "stop"
    assert resp.tool_calls == []
    assert resp.content == "Based on the tool result: 22C sunny"


def test_tool_selection_overlap_tie_breaking_and_argument_extraction() -> None:
    tools = [
        {
            "name": "lookup_weather",
            "description": "Check weather conditions and forecast",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "days": {"type": "integer"},
                    "detailed": {"type": "boolean"},
                },
            },
        },
        {
            "name": "backup_weather",
            "description": "Check weather conditions and forecast",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        },
    ]
    client = FakeLLM()
    resp = client.chat(
        [{"role": "user", "content": "Check weather forecast in 'New York' for 5 days? yes"}],
        tools=tools,
    )
    assert resp.finish_reason == "tool_calls"
    assert resp.content is None
    assert len(resp.tool_calls) == 1
    tc = resp.tool_calls[0]
    assert tc.id == "call_1"
    assert tc.name == "lookup_weather"
    assert tc.arguments == {"city": "New York", "days": 5, "detailed": True}


def test_tool_selection_extracts_capitalized_phrase_and_no_match_falls_back() -> None:
    tools = [
        {
            "name": "get_weather",
            "description": "Fetch weather for a city",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        }
    ]
    client = FakeLLM()
    hit = client.chat(
        [{"role": "user", "content": "What is the weather in Tokyo?"}],
        tools=tools,
    )
    assert hit.finish_reason == "tool_calls"
    assert hit.tool_calls[0].arguments == {"city": "Tokyo"}

    miss = client.chat(
        [{"role": "user", "content": "Tell me about quantum computing"}],
        tools=tools,
    )
    assert miss.finish_reason == "stop"
    assert miss.tool_calls == []
    assert miss.content is not None and miss.content.startswith("(fake model) I received:")


def test_tool_call_ids_increment_across_calls() -> None:
    tools = [
        {
            "name": "calc_sum",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            },
        }
    ]
    client = FakeLLM()
    r1 = client.chat([{"role": "user", "content": "Add numbers 1.5 and 2.5"}], tools=tools)
    r2 = client.chat([{"role": "user", "content": "Add numbers 10 and 20"}], tools=tools)
    assert r1.tool_calls[0].id == "call_1"
    assert r1.tool_calls[0].arguments == {"a": 1.5, "b": 2.5}
    assert r2.tool_calls[0].id == "call_2"
    assert r2.tool_calls[0].arguments == {"a": 10.0, "b": 20.0}


def test_response_format_json_parses_and_preserves_keys() -> None:
    client = FakeLLM()
    fmt = {
        "type": "json",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "verified": {"type": "boolean"},
            },
        },
    }
    resp = client.chat(
        [{"role": "user", "content": "name is Alice Smith, age 28, verified true."}],
        response_format=fmt,
    )
    assert resp.finish_reason == "stop"
    parsed = json.loads(resp.content or "")
    assert list(parsed.keys()) == ["name", "age", "verified"]
    assert parsed == {"name": "Alice Smith", "age": 28, "verified": True}


def test_rag_hit_returns_first_sentence_with_citation() -> None:
    client = FakeLLM()
    messages = [
        {
            "role": "system",
            "content": (
                "Context:\n"
                "[1] Pandas handles tabular data frames. It works well for CSV files.\n"
                "[2] PyTorch builds neural networks on tensors. It supports autograd."
            ),
        },
        {"role": "user", "content": "Which library builds neural networks?"},
    ]
    resp = client.chat(messages)
    assert resp.content == "PyTorch builds neural networks on tensors. [2]"


def test_rag_miss_returns_exact_unknown_message() -> None:
    client = FakeLLM()
    messages = [
        {
            "role": "user",
            "content": (
                "Context:\n"
                "[1] Bananas are yellow fruits.\n"
                "[2] Apples grow on trees.\n\n"
                "How do satellites orbit?"
            ),
        }
    ]
    resp = client.chat(messages)
    assert resp.content == "I don't know based on the provided context."


def test_knowledge_lookup_and_pirate_system_message() -> None:
    client = FakeLLM()
    rag_reply = client.chat([{"role": "user", "content": "What is RAG?"}]).content
    assert rag_reply is not None and "Retrieval-Augmented Generation" in rag_reply

    pirate_reply = client.chat(
        [
            {"role": "system", "content": "You are a helpful pirate captain."},
            {"role": "user", "content": "Tell me something cool about space travel"},
        ]
    ).content
    assert pirate_reply is not None
    assert pirate_reply.startswith("Arr! (fake model) I received:")


def test_fallback_truncates_to_twelve_tokens() -> None:
    client = FakeLLM()
    long_prompt = " ".join(f"w{i}" for i in range(20))
    resp = client.chat([{"role": "user", "content": long_prompt}])
    expected_prefix = "(fake model) I received: " + " ".join(f"w{i}" for i in range(12))
    assert resp.content == expected_prefix


def test_temperature_determinism_same_and_different_seeds() -> None:
    msg = [{"role": "user", "content": "hello world"}]
    c1 = FakeLLM(seed=0)
    c2 = FakeLLM(seed=0)
    seq1 = [c1.chat(msg, temperature=0.7).content for _ in range(4)]
    seq2 = [c2.chat(msg, temperature=0.7).content for _ in range(4)]
    assert seq1 == seq2

    c3 = FakeLLM(seed=3)
    assert (
        FakeLLM(seed=0).chat(msg, temperature=0.7).content
        != c3.chat(msg, temperature=0.7).content
    )


def test_embed_deterministic_normalized_synonyms_and_empty() -> None:
    client = FakeLLM(embed_dim=64)
    v1 = client.embed(["cheap car"])[0]
    v2 = client.embed(["cheap car"])[0]
    assert v1 == v2
    assert len(v1) == 64
    assert math.isclose(math.sqrt(sum(x * x for x in v1)), 1.0, rel_tol=1e-4)

    v_syn = client.embed(["affordable automobile"])[0]
    v_other = client.embed(["fast kitten"])[0]
    assert cosine(v1, v_syn) > cosine(v1, v_other)

    v_refund_a = client.embed(["money back"])[0]
    v_refund_b = client.embed(["reimbursement"])[0]
    assert math.isclose(cosine(v_refund_a, v_refund_b), 1.0, rel_tol=1e-5)

    v_empty = client.embed([""])[0]
    assert v_empty == [0.0] * 64
    assert cosine(v_empty, v1) == 0.0
    assert cosine([], []) == 0.0


def test_cosine_mismatched_lengths_raises_value_error() -> None:
    with pytest.raises(ValueError, match="same length"):
        cosine([1.0, 0.0], [1.0])


def test_priority_tools_over_json_and_json_over_rag() -> None:
    client = FakeLLM()
    tools = [
        {
            "name": "search_docs",
            "description": "Search docs for info",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}},
        }
    ]
    fmt = {
        "type": "json",
        "schema": {"type": "object", "properties": {"topic": {"type": "string"}}},
    }
    r1 = client.chat(
        [{"role": "user", "content": "Search docs for 'RAG'"}],
        tools=tools,
        response_format=fmt,
    )
    assert r1.finish_reason == "tool_calls"

    r2 = client.chat(
        [
            {
                "role": "system",
                "content": "Context:\n[1] Python is a language.\n[2] RAG retrieves documents.",
            },
            {"role": "user", "content": "topic is Python."},
        ],
        response_format=fmt,
    )
    assert json.loads(r2.content or "") == {"topic": "Python"}

