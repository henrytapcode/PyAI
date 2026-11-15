# Build an eval set and score retrieval hit rate

**What it shows:** Scoring top-2 document retrieval across a 6-question shop eval set while skipping unanswerable questions from the `hit_rate` denominator.

**Step by step**
1. Lines 5–13 define the 7-chunk shop knowledge base (`refunds.md`, `shipping.md`, `warranty.md`, `hours.md`, `pickup.md`, `payment.md`, `loyalty.md`).
2. Lines 15–22 define the 6-question `eval_set`, including one paraphrase (`q5`) and one unanswerable crypto question (`q6` with `expected_source=None`).
3. Lines 25–35 implement `hit_rate(results, k)` so `None` targets are skipped before counting hits.
4. Lines 38–54 embed all documents once with `FakeLLM(embed_dim=256)`, retrieve the top 2 sources per question, print the per-question trace table, and report `hit@2: 4/5 (0.8)`.

**Notice:** `q5` misses `refunds.md` at `k=2` (`hours.md` and `payment.md` rank higher), while `q6` is shown as `skip` rather than counted as a retrieval failure.

**Try it yourself:** Change `[:2]` to `[:3]` in the retrieval loop and `hit_rate(results, 3)` at the bottom to watch `q5` become a hit (`5/5 = 1.0`).
