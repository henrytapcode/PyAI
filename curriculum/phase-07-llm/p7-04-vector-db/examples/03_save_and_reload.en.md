# Save, reload, and delete in VectorStore

**What it shows:** Serializing a `VectorStore` to a JSON string, reloading it with zero `embed()` calls, and deleting a record cleanly without breaking remaining vector alignments.

**Step by step**
1. Lines 7–14 wrap `FakeLLM` in `CountingClient` to count every call to `embed()`.
2. Lines 51–67 serialize `ids`, `texts`, `metadatas`, and `vectors` to JSON (`to_json`) and reconstruct the store and NumPy matrix directly from those saved floats (`from_json`).
3. Lines 70–83 add three chunks (`1` embed call), reload into a fresh store (`0` embed calls during `from_json`), confirm identical search hits, then `delete("c2")` and verify `c1` stays aligned at `0.775`.

**Notice:** `from_json()` uses `reload_client` only later when embedding the new query `"money back for laptop"`, saving the cost of re-embedding the stored collection.

**Try it yourself:** Delete `"c1"` as well and call `reloaded.search("cheap car", k=1)` to confirm `"c3"` remains intact at row `0`.
