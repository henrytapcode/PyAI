# RAG FastAPI service basics

**What it shows:** How `create_app` embeds all 6 FAQ documents once at startup, serves `/health`, cites sources on `/ask`, and refuses unanswerable questions without calling `chat()`.

**Step by step**
1. Lines 17–28 define `SpyClient` to record every `embed` batch size and `chat` call around `FakeLLM(embed_dim=256)`.
2. Lines 36–70 define `create_app`, which embeds `DOCS` once into `doc_vecs` and attaches `/health` and `/ask` inside its closure.
3. Lines 74–87 send a `/health` request plus three `/ask` questions—two answerable (`refunds`, `shipping`) and one unanswerable (`crypto`)—and print status, sources, answers, and call counts.

**Notice:** `index_embed` stays `1` across all requests, while `chat` runs `2` times instead of `3` because the crypto question leaves `hits` empty and returns a refusal immediately.

**Try it yourself:** Raise `min_score` from `0.2` to `0.5` in `create_app` and see which questions still clear the retrieval threshold.
