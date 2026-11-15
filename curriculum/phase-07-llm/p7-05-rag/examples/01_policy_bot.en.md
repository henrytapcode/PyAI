# Shop policy RAG bot

**What it shows:** Answering policy questions from four small documents with verified `sources`, while skipping the LLM call completely on off-topic questions.

**Step by step**
1. Lines 7–12 store four short shop policy snippets, each tagged with its `source` filename.
2. Lines 15–22 subclass `FakeLLM` as `CountingLLM` to track how many times `chat()` is actually called.
3. Lines 25–47 define `ask_bot()`, which retrieves top-`k` matches, returns `"I don't know."` early when the best score is below `min_score=0.2`, and otherwise builds a `Context:` prompt and maps `[n]` citations back to `sources`.
4. Lines 50–62 embed all documents once and ask two policy questions plus one unrelated discount question.

**Notice:** On `"Do you offer student discounts?"`, the best retrieval score falls below `min_score`, so `ask_bot()` returns `"I don't know."` and `Total chat calls` stays `2` instead of `3`.

**Try it yourself:** Lower `min_score` to `0.0` in `ask_bot()` and watch `Total chat calls` increase to `3` while the model still refuses based on the context.
