# Parsing model replies safely

**What it shows:** how to read JSON that comes from a language model, which is sometimes valid and sometimes chatty text, without ever crashing the pipeline.

**Step by step**
1. Line 7 calls `json.loads(text)`, which turns JSON text into a dict. It raises `json.JSONDecodeError` when the text is not valid JSON.
2. Line 8 reads the two fields we need. A missing field raises `KeyError`. If the JSON was something else, like a list, `data["label"]` raises `TypeError`.
3. Lines 9–10 handle bad JSON. `as err` gives us the error object, and `err.msg` is its short message (`Expecting value`).
4. Lines 11–12 handle missing fields or the wrong JSON shape with a tuple of two types.
5. Line 13 is the **fallback**: after any handled error we return a safe "unknown" result, so the caller always receives a dict with the same keys.
6. The loop at the end shows all four cases: good JSON, chatty text, a missing field, and good JSON again.

**Notice:** the order of these two `except` blocks does not matter, because neither type is a kind of the other. Order only matters when one type is a kind of another (see the tree in lesson section 3): Python uses the first block that matches.

**Try it yourself:** add the reply `'["spam", 0.9]'` to `replies`. Which message do you expect? (A list cannot be read with `["label"]`, so you get `JSON is missing a field`.)
