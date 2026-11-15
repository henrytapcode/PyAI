# Keyword search vs. semantic search

**What it shows:** Comparing exact-word overlap (`kw`) against embedding cosine similarity (`cos`) for three synonym queries across four documents.

**Step by step**
1. Lines 5–16 define four short documents and three queries written with synonyms (`"affordable automobile"`, `"rapid computer"`, `"reimbursement bug"`).
2. Lines 19–20 define `keyword_hits()`, which counts lowercased words shared between a query and a document.
3. Lines 23–24 embed all four documents once into `doc_matrix` with `FakeLLM(embed_dim=256)`.
4. Lines 26–34 print a compact table showing `kw` and `cos` for every `(query, doc)` pair.

**Notice:** Every single `kw` score is `0` because the queries share zero exact words with the documents, whereas cosine similarity cleanly spots the intended match (`0.866`, `0.707`, `0.707`).

**Try it yourself:** Add `"car"` to `QUERIES[0]` and watch `kw` jump from `0` to `1` on `doc0`.
