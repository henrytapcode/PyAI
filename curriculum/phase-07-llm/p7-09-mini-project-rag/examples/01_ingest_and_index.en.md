# Ingest, chunk, and retrieve top-k FAQ chunks

**What it shows:** Splitting an 8-page FAQ corpus with sentence and word-window chunking, indexing sentence chunks once with `FakeLLM(embed_dim=256)`, and retrieving top-2 hits with `np.argsort(-scores, kind="stable")`.

**Step by step**
1. Lines 6–15 define the 8 shop FAQ pages.
2. Lines 18–37 define `chunk_docs(raw_docs, mode, size, overlap)` producing `<source>#<n>` chunk dictionaries.
3. Lines 40–43 print chunk counts (`24` sentence chunks vs `33` word-window chunks) and sample IDs.
4. Lines 45–54 embed all sentence chunks once, embed the warranty question, and print the top-2 scored chunks.

**Notice:** Sentence chunking produces fewer, cleaner chunks (`24` vs `33`), and `warranty.md#0` lands at rank `#1` (`0.625`) with the exact `"12 months"` sentence intact.

**Try it yourself:** Change `sent_chunks` in line 46 to `word_chunks` and inspect how the rank `#1` text changes when words are sliced by fixed 8-word windows.
