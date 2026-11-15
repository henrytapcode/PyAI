# Full dev comparison and one-time test report

**What it shows:** Comparing three RAG configurations on `dev_set`, selecting the winner (`sent k=2 m=0.2`) by `facts`, scoring `test_set` once, and reporting every dev and test failure honestly.

**Step by step**
1. Lines 17–40 split the 12 eval questions cleanly into `dev_set` (8) and `test_set` (4).
2. Lines 56–92 evaluate one `(mode, k, min_score)` configuration and classify failures into `"retrieval_miss"`, `"answer_miss"`, or `"no_refusal"`.
3. Lines 99–113 compare all three candidates on `dev_set` and pick the winner strictly from dev metrics.
4. Lines 114–120 score `test_set` once with the winning configuration and print both dev and test failures.

**Notice:** The winning configuration (`sent k=2 m=0.2`) gets `5/6 (83%)` facts on dev (`d6: answer_miss`, `d8: no_refusal`) and `2/3 (67%)` facts on test (`t3: answer_miss`), showing why raw counts and failure reasons matter more than chasing 100%.

**Try it yourself:** Remove `test_res` and re-run after changing `min_score` to `0.15` on `dev_set` only—does `dev` change at all?
