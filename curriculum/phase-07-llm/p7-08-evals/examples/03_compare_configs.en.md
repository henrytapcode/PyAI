# Compare two RAG configurations on the same eval set

**What it shows:** Running `k=1` versus `k=3` on the exact same 6-question eval set, printing raw counts alongside percentages, and listing the individual questions that changed.

**Step by step**
1. Lines 48–75 define `run_config(k)`, which embeds questions once against the pre-embedded `doc_matrix`, retrieves top-`k` chunks, generates answers, and aggregates counts.
2. Lines 78–86 run `k=1` and `k=3` and print a compact summary table with `hit@k`, `facts`, `faithful`, and `idk` counts.
3. Lines 88–91 compare per-question `(hit, facts)` tuples between `k=1` and `k=3` and print every changed question.

**Notice:** Raising `k` from `1` to `3` improves `hit@k` (`3/5` to `5/5`) and `facts` (`3/5` to `4/5`) by fixing `q2`, yet degrades `idk` (`1/1` to `0/1`) because `payment.md` slips into `q6`'s top 3 and triggers a wrong answer.

**Try it yourself:** Add `k=2` to the `for k in (1, 3):` loop and compare its summary row against `k=1` and `k=3`.
