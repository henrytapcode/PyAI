# Shop FAQ semantic search

**What it shows:** Embedding a shop's FAQ list once into a matrix and answering customer questions with top-1 dot-product ranking plus a minimum score threshold.

**Step by step**
1. Lines 5–20 define six `FAQS`, three `QUERIES` (including one unrelated weather question), and `MIN_SCORE = 0.3`.
2. Lines 22–23 initialize `FakeLLM(embed_dim=256)` and embed all six FAQs in a single batch into `doc_matrix`.
3. Lines 25–32 embed each customer query, score every FAQ at once with `doc_matrix @ q_vec`, and pick the top-1 match using `np.argsort(-scores, kind="stable")[0]`.
4. Lines 30–32 print `"no good match"` when `best_score < MIN_SCORE`, preventing an unrelated weather query from matching a shop policy.

**Notice:** `"Want full money back"` matches `"Full refund available within 30 days."` (`0.471`) even though they share no words, because `FakeLLM` maps `"money back"` to `"refund"`.

**Try it yourself:** Lower `MIN_SCORE` to `0.0` or add a fourth query `"cheap vehicle insurance"` and check which FAQ wins.
