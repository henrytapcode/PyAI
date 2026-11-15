# `pyai_llm`

Deterministic fake LLM and embedding client using only the Python standard library. Designed for offline lessons, browser execution (Pyodide), local runners, and automated tests without network access or API keys.

## Installation (workspace)

`pyai-llm` is installed as an editable local package in the workspace:

```bash
uv sync
uv run python -I -c "import pyai_llm; print(pyai_llm.__version__)"
```

## Quick Examples

### Basic chat and system messages

```python
from pyai_llm import FakeLLM

client = FakeLLM()
resp = client.chat([
    {"role": "system", "content": "You are a pirate assistant."},
    {"role": "user", "content": "What is RAG?"},
])
print(resp.content)
print(resp.usage)
```

### Scripted replies and tool calls

```python
from pyai_llm import FakeLLM

client = FakeLLM(script=[
    {"tool_calls": [{"name": "get_weather", "arguments": {"city": "Hanoi"}}]},
    "It is sunny in Hanoi.",
])
first = client.chat([{"role": "user", "content": "Weather in Hanoi?"}])
second = client.chat([{"role": "user", "content": "Continue"}])
```

### Automatic tool selection and tool results

```python
from pyai_llm import FakeLLM

tools = [{
    "name": "get_weather",
    "description": "Get weather forecast for a city",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
}]
client = FakeLLM()
messages = [{"role": "user", "content": "What is the weather in Tokyo?"}]
call_resp = client.chat(messages, tools=tools)
tc = call_resp.tool_calls[0]

messages.append({"role": "assistant", "content": None, "tool_calls": [tc]})
messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.name, "content": "24C, clear"})
final_resp = client.chat(messages, tools=tools)
print(final_resp.content)  # Based on the tool result: 24C, clear
```

### Structured JSON output

```python
import json
from pyai_llm import FakeLLM

client = FakeLLM()
resp = client.chat(
    [{"role": "user", "content": "name is Alice, age 28, active yes."}],
    response_format={
        "type": "json",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "active": {"type": "boolean"},
            },
        },
    },
)
print(json.loads(resp.content))
```

### RAG with `Context:` and numbered chunks

```python
from pyai_llm import FakeLLM

client = FakeLLM()
resp = client.chat([
    {
        "role": "system",
        "content": "Context:\n[1] Python 3.11 adds speedups. It is widely used.\n[2] RAG retrieves chunks.",
    },
    {"role": "user", "content": "What does RAG retrieve?"},
])
print(resp.content)  # RAG retrieves chunks. [2]
```

### Temperature, `max_tokens`, and `fail_times`

```python
from pyai_llm import FakeLLM, RateLimitError

# Seeded randomness with temperature > 0
c = FakeLLM(seed=3)
print(c.chat([{"role": "user", "content": "hello"}], temperature=0.7, max_tokens=5))

# Retry simulation with fail_times
flaky = FakeLLM(fail_times=1, script=["ok"])
try:
    flaky.chat([{"role": "user", "content": "ping"}])
except RateLimitError:
    print(flaky.chat([{"role": "user", "content": "ping"}]).content)
```

### Embeddings and `cosine` similarity

```python
from pyai_llm import FakeLLM, cosine

client = FakeLLM(embed_dim=64)
v1, v2, v3 = client.embed(["cheap car", "affordable automobile", "fast kitten"])
print(round(cosine(v1, v2), 3) > round(cosine(v1, v3), 3))  # True
```
