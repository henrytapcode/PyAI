Write `evaluate_bot(answer_fn, eval_set)` and `report_lines(summary)` to score a RAG bot deterministically and format an honest line-by-line report. Write your code inside both functions and `return` the results.

**Example**

```python
summary = evaluate_bot(bot_fn, eval_set)
# {
#     "n": 7, "hits": 4, "n_answerable": 5, "facts_ok": 3,
#     "idk_ok": 1, "n_unanswerable": 2,
#     "failures": [("q3", "answer_miss"), ("q6", "no_refusal")],
# }
report_lines(summary)
# [
#     "hit@k: 4/5 (80%)",
#     "facts: 3/5 (60%)",
#     "refusals: 1/2 (50%)",
#     "FAIL q3: answer_miss",
#     "FAIL q6: no_refusal",
#     "failures: 2",
# ]
```

**Rules**

- `answer_fn(question)` returns `{"answer": str, "sources": list[str], "retrieved": list[str]}`.
- In `evaluate_bot`:
  - Return a dict with exact keys: `"n"`, `"hits"`, `"n_answerable"`, `"facts_ok"`, `"idk_ok"`, `"n_unanswerable"`, `"failures"`.
  - Do not modify `eval_set`.
  - For unanswerable rows (`row["expected_source"] is None`):
    - Increment `n_unanswerable`.
    - Pass (`idk_ok += 1`) only if `"i don't know"` appears in `out["answer"].lower()` **and** `out["sources"] == []`; otherwise append `(row["id"], "no_refusal")` to `failures`.
  - For answerable rows (`row["expected_source"] is not None`):
    - Increment `n_answerable`.
    - `hit` is `row["expected_source"] in out["retrieved"]`; increment `hits` if `hit`.
    - `facts` is `all(f.lower() in out["answer"].lower() for f in row["expected_facts"])`; increment `facts_ok` if `facts`.
    - If not `hit`, append `(row["id"], "retrieval_miss")` (even if facts matched in the answer); otherwise if not `facts`, append `(row["id"], "answer_miss")`.
  - Keep `failures` in the exact order of `eval_set`.
- In `report_lines`:
  - Format each metric ratio as `"n/a"` when the denominator is `0`, or `f"{num}/{den} ({round(num / den * 100)}%)"` otherwise.
  - Return lines in exact order: `"hit@k: ..."`, `"facts: ..."`, `"refusals: ..."`, one `"FAIL <id>: <reason>"` line per failure in order, and `"failures: <count>"`.
