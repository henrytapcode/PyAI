# LLM chat endpoint with token counting

**What it shows:** Wrapping `FakeLLM` behind a `POST /chat` endpoint, accumulating returned `tokens` across requests, and letting Pydantic reject an invalid `temperature`.

**Step by step**
1. Lines 8–9 create `app` and instantiate `llm = FakeLLM(seed=0)` once at module level.
2. Lines 12–14 define `ChatRequest` requiring a non-empty `message` and `temperature` between `0.0` and `1.0`.
3. Lines 17–23 forward the validated message and temperature to `llm.chat(...)` and return both `answer` and `tokens`.
4. Lines 26–44 send three valid chat prompts, sum `total_tokens` (`82`), and then send `temperature=2` to observe the automatic `422` validation error.

**Notice:** Returning `tokens` in the JSON response lets callers and monitoring tools track LLM usage without re-tokenizing on the client, and `FakeLLM` is never even called when `temperature=2` fails validation.

**Try it yourself:** Pass `"temperature": 0.5` in the first three requests and check whether `answer` or `tokens` changes with `FakeLLM(seed=0)`.
