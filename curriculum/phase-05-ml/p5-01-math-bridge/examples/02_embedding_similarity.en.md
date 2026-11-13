# Nearest document by cosine similarity

**What it shows:** Comparing a query vector against four small 4D document embeddings using cosine similarity to pick the closest match.

**Step by step**
1. Line 4 defines a 4-number `query` embedding.
2. Lines 6–11 hold four labelled document vectors of the same length.
3. Line 15 computes the query's length `q_norm` once with `np.linalg.norm(query)` so we do not recompute it in the loop.
4. Lines 17–24 divide each dot product `query @ vec` by `q_norm * np.linalg.norm(vec)`, print the rounded similarity, and track the highest match.

**Notice:** `refund_policy` scores `0.99` because its numbers point in almost the same direction as `query`, even though `shipping_faq` also shares positive entries.

**Try it yourself:** Multiply `refund_policy` by `2.0` (making the arrow twice as long) and re-run — notice its cosine similarity stays `0.99`.
