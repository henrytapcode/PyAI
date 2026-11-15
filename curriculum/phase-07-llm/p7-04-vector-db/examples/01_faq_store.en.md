# Bilingual FAQ vector store

**What it shows:** Storing eight bilingual FAQ chunks with `topic` and `lang` metadata in a `VectorStore`, then answering unfiltered and metadata-filtered queries.

**Step by step**
1. Lines 7–54 define `Hit` and `VectorStore`, validating unique IDs, batch-embedding texts once in `add()`, and pre-filtering metadata in `search()`.
2. Lines 57–69 define eight bilingual `CHUNKS` with `topic` and `lang` metadata and insert them all in one `store.add(...)` call.
3. Lines 71–79 run three queries: two unfiltered synonym queries (`"money back"` and `"affordable vehicle"`) and one filtered query restricting `lang` to `"vi"` and `topic` to `"support"`.

**Notice:** On the third query, `faq2` (`"Fast laptop repair in two days."`) is excluded before ranking because `lang` is `"en"`, so `faq6` takes rank 1 cleanly.

**Try it yourself:** Change the third query's filter to `{"lang": "en", "topic": "support"}` and verify that `faq2` and `faq4` are returned instead.
