# Fault-tolerant tool dispatch

**What it shows:** A `dispatch()` helper handling five `ToolCall` cases—valid with empty optional arg, unknown tool, missing required arg, wrong argument type, and a function raising `ValueError`—without crashing.

**Step by step**
1. Lines 9–22 define `get_weather()` (which raises `ValueError` for unknown cities), `add_tax()` (which rejects non-numeric `price` with `TypeError`), plus `REGISTRY` and `REQUIRED`.
2. Lines 25–38 implement `dispatch()`: it rejects unknown tool names, checks required keys against `("", None)`, strips empty optional placeholders, runs `registry[call.name](**clean)` inside `try/except`, and formats `dict` outputs with `json.dumps()`.
3. Lines 41–50 construct five `ToolCall` objects covering one valid call and four failure modes, printing the returned string for each.

**Notice:** Instead of crashing on `call_2` through `call_5`, `dispatch()` returns `"error: ..."` strings that can be sent straight back to an LLM as `tool` messages.

**Try it yourself:** Add a valid `add_tax` `ToolCall` with `{"price": 20.0}` to `test_calls` and verify `dispatch()` returns `"22.0"`.
