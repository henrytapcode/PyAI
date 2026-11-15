# Score answer facts and faithfulness

**What it shows:** Running the full `FakeLLM` RAG pipeline on the eval set to measure `facts`, `faithful`, and `"I don't know"` refusals, then catching a scripted hallucination.

**Step by step**
1. Lines 25–45 define `content_words()` and `score_answer()`, which checks lowercase `expected_facts` containment and verifies every content word (`len >= 4`, excluding `[n]` citations) appears in `context`.
2. Lines 48–66 retrieve the top 2 chunks per question, call `client.chat(...)`, and print `facts`, `faithful`, and `idk` for `q1`–`q6`.
3. Lines 69–76 create a separate `FakeLLM(script=[...])` client that outputs `"Refunds are issued within 30 days with free courier pickup. [1]"` and score it against `q1_context`.

**Notice:** The scripted reply contains `"30 days"` so `facts=1.0`, yet `faithful` catches it as `False` and lists `['with', 'free', 'courier', 'pickup']` as unsupported claims.

**Try it yourself:** Change the scripted reply to `"Refunds are issued within 30 days of purchase. [1]"` and verify that `faithful` flips back to `True` with `unsupported: []`.
