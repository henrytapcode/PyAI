# Four-turn FAQ chat with follow-up rewriting

**What it shows:** Running a 4-turn FAQ conversation where short follow-up questions are deterministically rewritten with the previous user question before retrieval, while out-of-scope questions refuse cleanly.

**Step by step**
1. Lines 6–25 index the 8 shop FAQ pages into 24 sentence chunks using `FakeLLM(embed_dim=256)`.
2. Lines 28–35 define `rewrite_query(question, history)` to prepend the latest user question whenever a turn has at most 4 words or starts with `"what about"`, `"and"`, or `"how about"`.
3. Lines 38–61 define `ask_turn(question, history)` to retrieve top-2 chunks above `min_score=0.2`, validate `[n]` citations, and append both turns to `history`.
4. Lines 64–76 run 4 turns—an initial pickup question, a follow-up `"And photo ID?"`, a weekday support question, and an unanswerable crypto question—and print each turn's fields.

**Notice:** Without rewriting, `"And photo ID?"` would lack the word `"pickup"` in the prompt; prepending turn 1's question lets turn 2 retrieve `pickup.md` and answer `"Bring a photo ID at pickup. [1]"`, whereas turn 4 produces no chunks above `min_score` and returns empty `sources`.

**Try it yourself:** Replace `"And photo ID?"` with `"What about express?"` after asking `"How much does delivery cost?"` on turn 1, and watch the rewritten query pull `shipping.md`.
