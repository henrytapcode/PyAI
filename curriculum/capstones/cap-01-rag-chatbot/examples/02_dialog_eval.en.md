# Golden dialog evaluation and baseline diff

**What it shows:** Scoring two 2-turn golden dialogs turn by turn and diffing the candidate run against a baseline to surface both `fixed` improvements and `broken` regressions.

**Step by step**
1. Lines 17–30 define two golden dialogs (`d1` with a follow-up turn, `d2` with an answerable turn and a refusal turn).
2. Lines 41–73 define `eval_dialogs(rewrite, min_score)` to score each turn against `expected_source`, `expected_facts`, or expected refusal.
3. Lines 76–77 run the baseline (`rewrite=False, min_score=0.2`) and candidate (`rewrite=True, min_score=0.35`).
4. Lines 79–88 compute `fixed` and `broken` turns and print the comparison table.

**Notice:** Both runs score `3/4 (75%)` overall, yet the per-turn diff reveals a hidden trade-off: rewriting fixed `d1#t2`, while raising `min_score` to `0.35` broke `d2#t1`.

**Try it yourself:** Change `min_score=0.35` on line 77 to `min_score=0.25` and confirm that `d1#t2` stays fixed while `broken` drops to `[]`.
