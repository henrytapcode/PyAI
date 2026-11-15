# Answer direct, paraphrased, and out-of-scope questions

**What it shows:** Running the end-to-end RAG responder across three realistic question types—a direct question, a paraphrase, and an unanswerable question—while validating `[n]` citations.

**Step by step**
1. Lines 18–25 build the sentence-chunk index once with `FakeLLM(embed_dim=256)`.
2. Lines 28–50 implement `answer_with_sources()`, filtering hits with `min_score=0.2`, sending `Context:` to `FakeLLM.chat()`, and extracting valid `source` names from `[n]`.
3. Lines 56–65 run the bot on `"direct"`, `"paraphrase"`, and `"out_of_docs"` queries and print each answer and source list.

**Notice:** The `"paraphrase"` query (`"Can I get money back within a month?"`) retrieves `refunds.md`, yet `FakeLLM.chat()` checks raw word overlap (`>= 2` words) without synonym expansion and returns `"I don't know based on the provided context."` with `sources: []`.

**Try it yourself:** Replace `"money back"` with `"refunds"` in the second query and re-run to watch `sources` flip to `['refunds.md']`.
