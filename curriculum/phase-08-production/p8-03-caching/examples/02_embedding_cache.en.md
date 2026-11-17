# Batch embedding cache when re-indexing documents

**What it shows:** Re-indexing 6 documents after editing 2 of them so `client.embed()` is called only for the 2 changed texts while all 6 output vectors stay in exact document order.

**Step by step**
1. Lines 6–26 define `embed_batch_cached(client, model, texts, cache)`, collecting unique missing texts under `(model, text)`, calling `client.embed(missing)` once for the whole missing batch, and rebuilding `ordered` in the original list order.
2. Lines 29–44 index 6 initial documents (`docs_v1`), sending `6/6` texts to `embed()`.
3. Lines 46–55 edit indices `1` and `4` in `docs_v2`, re-index (`2/6` texts sent), and verify `match: True` against a fresh uncached `client.embed(docs_v2)`.

**Notice:** Keying by `(model, text)` lets you keep unchanged document vectors across partial edits while ensuring a model upgrade (`"embed-v2"`) never mixes incompatible vectors.

**Try it yourself:** Change `model` from `"embed-v1"` to `"embed-v2"` before the second call and verify that all `6/6` texts are sent again.
