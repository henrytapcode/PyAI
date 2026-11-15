"""Deterministic fake LLM client for offline curriculum exercises and tests."""

from __future__ import annotations

import json
import math
import random
import re
import zlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

__version__ = "0.1.0"

__all__ = [
    "ChatResponse",
    "FakeLLM",
    "RateLimitError",
    "ToolCall",
    "Usage",
    "__version__",
    "cosine",
    "count_tokens",
]

_VALID_ROLES = frozenset({"system", "user", "assistant", "tool"})
_TOKEN_RE = re.compile(r"\w+|[^\w\s]")
_WORD_RE = re.compile(r"\w+")
_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
_QUOTED_RE = re.compile(r'(?<!\w)"([^"]*)"(?!\w)|(?<!\w)\'([^\']*)\'(?!\w)')
_CAP_PHRASE_RE = re.compile(r"\b[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)*\b")
_FIRST_SENTENCE_RE = re.compile(r"^.+?[.!?](?=\s|$)")
_RAG_CHUNK_RE = re.compile(r"^\s*\[(\d+)\]\s*(.+)$")
_PHRASE_SYNONYMS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bmoney\s+back\b"), "refund"),
)

_SYNONYMS: dict[str, str] = {
    "car": "car",
    "automobile": "car",
    "vehicle": "car",
    "refund": "refund",
    "reimbursement": "refund",
    "laptop": "computer",
    "notebook": "computer",
    "computer": "computer",
    "cat": "cat",
    "kitten": "cat",
    "feline": "cat",
    "doctor": "doctor",
    "physician": "doctor",
    "cheap": "cheap",
    "inexpensive": "cheap",
    "affordable": "cheap",
    "fast": "fast",
    "quick": "fast",
    "rapid": "fast",
    "error": "error",
    "bug": "error",
    "failure": "error",
    "happy": "happy",
    "glad": "happy",
    "joyful": "happy",
    "big": "big",
    "large": "big",
    "huge": "big",
}

_KNOWLEDGE: tuple[tuple[tuple[str, ...], str], ...] = (
    (
        ("what is rag", "retrieval-augmented generation", "rag"),
        "RAG (Retrieval-Augmented Generation) retrieves relevant documents and "
        "adds them to the prompt before generating an answer.",
    ),
    (
        ("embedding", "embeddings"),
        "An embedding maps text into a dense vector of numbers so similar "
        "meanings sit close together.",
    ),
    (
        ("tokenization", "what is a token", "tokens"),
        "Tokens are the small text pieces (words, subwords, or punctuation) "
        "that an LLM reads and generates.",
    ),
    (
        ("temperature",),
        "Temperature controls randomness: 0 makes outputs deterministic, while "
        "higher values increase variety.",
    ),
    (
        ("cosine similarity",),
        "Cosine similarity measures the cosine of the angle between two "
        "vectors, ranging from -1 to 1.",
    ),
    (
        ("tool calling", "function calling"),
        "Tool calling lets an LLM return a structured function name and "
        "arguments so your program can run external actions.",
    ),
    (
        ("system prompt",),
        "A system prompt sets the assistant's role, tone, and constraints "
        "before the conversation begins.",
    ),
    (
        ("hallucination", "hallucinations"),
        "An LLM hallucination happens when the model states plausible-sounding "
        "but fabricated or ungrounded information.",
    ),
)

_TEMP_PREFIXES: tuple[str, ...] = ("", "Sure. ", "Here is what I know: ")


class RateLimitError(Exception):
    """Raised when the fake client simulates a rate limit failure."""


@dataclass
class Usage:
    """Token counts for a chat completion."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ToolCall:
    """A structured tool invocation requested by the fake model."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ChatResponse:
    """Response returned by :meth:`FakeLLM.chat`."""

    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"
    usage: Usage = field(default_factory=lambda: Usage(0, 0, 0))


def count_tokens(text: str) -> int:
    """Count word and punctuation tokens in ``text``."""
    if not text:
        return 0
    return len(_TOKEN_RE.findall(text))


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two numeric sequences."""
    if len(a) != len(b):
        raise ValueError(f"vectors must have the same length ({len(a)} != {len(b)})")
    if len(a) == 0:
        return 0.0
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    return dot / (norm_a * norm_b)


def _normalize_words(text: str) -> set[str]:
    """Lowercase, remove punctuation, and keep words with length >= 3."""
    cleaned = text.lower().replace("_", " ")
    return {word for word in _WORD_RE.findall(cleaned) if len(word) >= 3}


def _truncate_tokens(text: str, max_tokens: int) -> tuple[str, bool]:
    """Return ``(text_or_truncated, was_truncated)`` capped at ``max_tokens``."""
    matches = list(_TOKEN_RE.finditer(text))
    if len(matches) <= max_tokens:
        return text, False
    if max_tokens <= 0:
        return "", True
    return text[: matches[max_tokens - 1].end()], True


def _extract_capitalized_phrases(text: str) -> list[str]:
    """Find capitalized phrases not located at the start of a sentence."""
    phrases: list[str] = []
    for match in _CAP_PHRASE_RE.finditer(text):
        phrase = match.group(0)
        if phrase == "I":
            continue
        before = text[: match.start()].rstrip()
        if not before or before[-1] in ".!?\n":
            continue
        phrases.append(phrase)
    return phrases


def _extract_value_for_key(text: str, key: str) -> str | None:
    """Extract ``<key>: <val>`` or ``<key> is <val>`` up to comma or period."""
    variants = [re.escape(key)]
    if "_" in key:
        variants.append(re.escape(key.replace("_", " ")))
    key_pattern = "|".join(variants)
    pattern = re.compile(
        rf"\b(?:{key_pattern})(?:\s*:\s*|\s+is\s+)([^,.\n]+)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        value = value[1:-1]
    return value


def _extract_schema_values(
    text: str,
    properties: dict[str, Any],
    *,
    allow_key_patterns: bool,
) -> dict[str, Any]:
    """Extract typed values from ``text`` in schema ``properties`` order."""
    numbers = _NUMBER_RE.findall(text)
    quoted = [a or b for a, b in _QUOTED_RE.findall(text)]
    cap_phrases = _extract_capitalized_phrases(text)
    has_bool_true = bool(re.search(r"\b(?:yes|true)\b", text, re.IGNORECASE))

    num_idx = 0
    str_idx = 0
    cap_idx = 0
    result: dict[str, Any] = {}

    for key, spec in properties.items():
        prop_type = spec.get("type", "string") if isinstance(spec, dict) else "string"
        if prop_type == "integer":
            if num_idx < len(numbers):
                result[key] = int(float(numbers[num_idx]))
                num_idx += 1
            else:
                result[key] = 0
        elif prop_type == "number":
            if num_idx < len(numbers):
                result[key] = float(numbers[num_idx])
                num_idx += 1
            else:
                result[key] = 0.0
        elif prop_type == "boolean":
            result[key] = has_bool_true
        elif prop_type == "string":
            if allow_key_patterns:
                keyed = _extract_value_for_key(text, key)
                if keyed is not None:
                    result[key] = keyed
                    continue
            if str_idx < len(quoted):
                result[key] = quoted[str_idx]
                str_idx += 1
            elif cap_idx < len(cap_phrases):
                result[key] = cap_phrases[cap_idx]
                cap_idx += 1
            else:
                result[key] = ""
        else:
            result[key] = ""

    return result


def _parse_rag_context(content: str) -> tuple[list[tuple[int, str]], str]:
    """Extract numbered ``[n]`` chunks after ``Context:`` and remaining text."""
    lines = content.splitlines()
    chunks: list[tuple[int, str]] = []
    remaining: list[str] = []
    in_context = False

    for line in lines:
        stripped = line.strip()
        if not in_context:
            if stripped == "Context:":
                in_context = True
                continue
            remaining.append(line)
            continue

        match = _RAG_CHUNK_RE.match(line)
        if match:
            chunks.append((int(match.group(1)), match.group(2).strip()))
        elif not stripped:
            continue
        else:
            in_context = False
            remaining.append(line)

    return chunks, "\n".join(remaining).strip()


def _first_sentence(text: str) -> str:
    """Return the first sentence of ``text``."""
    stripped = text.strip()
    match = _FIRST_SENTENCE_RE.search(stripped)
    return match.group(0).strip() if match else stripped


def _validate_messages(messages: Sequence[dict[str, Any]]) -> None:
    """Validate chat message list structure, roles, and content."""
    if not isinstance(messages, (list, tuple)) or len(messages) == 0:
        raise ValueError("messages must be a non-empty list of message dicts")

    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            raise ValueError(f"message at index {idx} must be a dict")
        role = msg.get("role")
        if role not in _VALID_ROLES:
            raise ValueError(
                f"invalid role at index {idx}: {role!r}; "
                "expected 'system', 'user', 'assistant', or 'tool'"
            )
        if "content" not in msg:
            raise ValueError(f"message at index {idx} is missing required 'content'")
        content = msg["content"]
        allow_none = role == "assistant" and bool(msg.get("tool_calls"))
        if not isinstance(content, str) and not (allow_none and content is None):
            raise ValueError(f"message at index {idx} must have string 'content'")


class FakeLLM:
    """Deterministic in-memory LLM and embedding client for teaching and tests."""

    def __init__(
        self,
        seed: int = 0,
        script: list[str | dict[str, Any]] | None = None,
        fail_times: int = 0,
        embed_dim: int = 64,
    ) -> None:
        """Initialize the fake client with optional script, failures, and seed."""
        if fail_times < 0:
            raise ValueError("fail_times must be non-negative")
        if embed_dim <= 0:
            raise ValueError("embed_dim must be positive")
        self._seed = seed
        self._script = list(script) if script is not None else None
        self._script_index = 0
        self._fail_remaining = fail_times
        self._embed_dim = embed_dim
        self._tool_call_counter = 0
        self._chat_calls = 0

    def _next_tool_call_id(self) -> str:
        self._tool_call_counter += 1
        return f"call_{self._tool_call_counter}"

    def _consume_failure(self) -> None:
        if self._fail_remaining > 0:
            self._fail_remaining -= 1
            raise RateLimitError("rate limit exceeded, retry later")

    def chat(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.0,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> ChatResponse:
        """Return a deterministic :class:`ChatResponse` for ``messages``."""
        _validate_messages(messages)
        if temperature < 0:
            raise ValueError("temperature must be non-negative")
        if max_tokens is not None and max_tokens < 0:
            raise ValueError("max_tokens must be non-negative")

        self._consume_failure()
        call_index = self._chat_calls
        self._chat_calls += 1

        prompt_tokens = sum(count_tokens(m["content"] or "") + 4 for m in messages)

        content, tool_calls, finish_reason = self._decide_reply(
            messages=messages,
            temperature=temperature,
            tools=tools,
            response_format=response_format,
            call_index=call_index,
        )

        if content is not None and max_tokens is not None:
            content, truncated = _truncate_tokens(content, max_tokens)
            if truncated:
                finish_reason = "length"

        if content is not None:
            completion_tokens = count_tokens(content)
        else:
            completion_tokens = sum(
                count_tokens(tc.name) + count_tokens(json.dumps(tc.arguments))
                for tc in tool_calls
            )

        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        return ChatResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            usage=usage,
        )

    def _decide_reply(
        self,
        *,
        messages: list[dict[str, Any]],
        temperature: float,
        tools: list[dict[str, Any]] | None,
        response_format: dict[str, Any] | None,
        call_index: int,
    ) -> tuple[str | None, list[ToolCall], str]:
        # 1. Script overrides all other rules.
        if self._script is not None:
            if self._script_index >= len(self._script):
                raise IndexError(f"script exhausted after {len(self._script)} replies")
            item = self._script[self._script_index]
            self._script_index += 1
            if isinstance(item, str):
                return item, [], "stop"
            if isinstance(item, dict):
                if "tool_calls" in item:
                    calls: list[ToolCall] = []
                    for tc in item["tool_calls"]:
                        if isinstance(tc, ToolCall):
                            calls.append(
                                ToolCall(
                                    id=tc.id or self._next_tool_call_id(),
                                    name=tc.name,
                                    arguments=dict(tc.arguments),
                                )
                            )
                        else:
                            calls.append(
                                ToolCall(
                                    id=self._next_tool_call_id(),
                                    name=tc["name"],
                                    arguments=dict(tc.get("arguments", {})),
                                )
                            )
                    return item.get("content"), calls, item.get("finish_reason", "tool_calls")
                return item.get("content", ""), [], item.get("finish_reason", "stop")
            raise TypeError(f"unsupported script entry type: {type(item).__name__}")

        # 2. Tool result in the last message.
        if messages[-1]["role"] == "tool":
            return f"Based on the tool result: {messages[-1]['content']}", [], "stop"

        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )

        # 3. Tool selection by word overlap.
        if tools:
            user_words = _normalize_words(last_user)
            best_tool: dict[str, Any] | None = None
            best_score = 0
            for tool in tools:
                tool_text = f"{tool.get('name', '')} {tool.get('description', '')}"
                score = len(user_words & _normalize_words(tool_text))
                if score > best_score:
                    best_score = score
                    best_tool = tool
            if best_tool is not None:
                props = (best_tool.get("parameters") or {}).get("properties", {})
                args = _extract_schema_values(last_user, props, allow_key_patterns=False)
                call = ToolCall(
                    id=self._next_tool_call_id(),
                    name=best_tool["name"],
                    arguments=args,
                )
                return None, [call], "tool_calls"

        # 4. Structured JSON output.
        if isinstance(response_format, dict) and response_format.get("type") == "json":
            props = (response_format.get("schema") or {}).get("properties", {})
            payload = _extract_schema_values(last_user, props, allow_key_patterns=True)
            return json.dumps(payload, sort_keys=False), [], "stop"

        # 5. RAG context retrieval.
        rag_reply = self._try_rag(messages)
        if rag_reply is not None:
            return rag_reply, [], "stop"

        # 6. Normal deterministic reply.
        return self._normal_reply(messages, last_user, temperature, call_index), [], "stop"

    def _try_rag(self, messages: list[dict[str, Any]]) -> str | None:
        all_chunks: list[tuple[int, str]] = []
        last_user_idx = -1
        for idx in range(len(messages) - 1, -1, -1):
            if messages[idx]["role"] == "user":
                last_user_idx = idx
                break
        if last_user_idx == -1:
            return None

        question = messages[last_user_idx]["content"]
        for idx, msg in enumerate(messages):
            if msg["role"] not in ("system", "user"):
                continue
            chunks, remaining = _parse_rag_context(msg["content"])
            if chunks:
                all_chunks.extend(chunks)
                if idx == last_user_idx:
                    question = remaining

        if not all_chunks or not question:
            return None

        question_words = _normalize_words(question)
        best_chunk: tuple[int, str] | None = None
        best_overlap = 0
        for chunk_id, chunk_text in all_chunks:
            overlap = len(question_words & _normalize_words(chunk_text))
            if overlap > best_overlap:
                best_overlap = overlap
                best_chunk = (chunk_id, chunk_text)

        if best_chunk is not None and best_overlap >= 2:
            chunk_id, chunk_text = best_chunk
            return f"{_first_sentence(chunk_text)} [{chunk_id}]"
        return "I don't know based on the provided context."

    def _normal_reply(
        self,
        messages: list[dict[str, Any]],
        last_user: str,
        temperature: float,
        call_index: int,
    ) -> str:
        lowered = last_user.lower()
        base_reply: str | None = None
        for keywords, answer in _KNOWLEDGE:
            if any(re.search(rf"\b{re.escape(kw)}\b", lowered) for kw in keywords):
                base_reply = answer
                break

        if base_reply is None:
            snippet, _ = _truncate_tokens(last_user, 12)
            base_reply = f"(fake model) I received: {snippet}"

        if temperature > 0:
            rng = random.Random(self._seed * 1000 + call_index)
            prefix = rng.choice(_TEMP_PREFIXES)
            base_reply = f"{prefix}{base_reply}"

        is_pirate = any(
            m["role"] == "system" and "pirate" in (m["content"] or "").lower()
            for m in messages
        )
        if is_pirate:
            base_reply = f"Arr! {base_reply}"

        return base_reply

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Compute deterministic L2-normalized bag-of-words embeddings."""
        if isinstance(texts, str):
            raise TypeError("texts must be a sequence of strings, not a single str")
        self._consume_failure()
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        lowered = text.lower()
        for pattern, replacement in _PHRASE_SYNONYMS:
            lowered = pattern.sub(replacement, lowered)

        vec = [0.0] * self._embed_dim
        for word in _WORD_RE.findall(lowered):
            if len(word) > 3 and word.endswith("s"):
                word = word[:-1]
            canonical = _SYNONYMS.get(word, word)
            idx = zlib.crc32(canonical.encode("utf-8")) % self._embed_dim
            vec[idx] += 1.0

        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0.0:
            return vec
        return [round(v / norm, 6) for v in vec]
