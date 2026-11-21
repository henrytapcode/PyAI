# Virtual environment isolation

**What it shows:** why two projects can hold different versions of the same package, and how to check each environment against a required list.

**Step by step**
1. Lines 2–5 define two isolated project environments (`chatbot` and `evals`) with their installed package versions.
2. Line 7 defines the target versions we expect (`required`).
3. Lines 9–16 inspect each environment separately for missing packages and version mismatches.

**Notice:** `chatbot` has `pydantic` but an older `httpx`; `evals` has the right `httpx` but is missing `pydantic`. Neither environment affects the other.

**Try it yourself:** add `"pydantic": "2.6.0"` to `"evals"` and run again to see both lists become empty.
