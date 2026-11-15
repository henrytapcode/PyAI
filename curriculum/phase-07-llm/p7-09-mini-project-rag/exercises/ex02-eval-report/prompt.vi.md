Viết hai hàm `evaluate_bot(answer_fn, eval_set)` và `report_lines(summary)` để chấm bot RAG một cách tất định và định dạng báo cáo trung thực theo từng dòng. Viết code bên trong hai hàm và `return` kết quả.

**Ví dụ**

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

**Quy tắc**

- `answer_fn(question)` trả về `{"answer": str, "sources": list[str], "retrieved": list[str]}`.
- Trong `evaluate_bot`:
  - Trả về dict với đúng các khóa: `"n"`, `"hits"`, `"n_answerable"`, `"facts_ok"`, `"idk_ok"`, `"n_unanswerable"`, `"failures"`.
  - Không làm thay đổi `eval_set`.
  - Với câu không trả lời được (`row["expected_source"] is None`):
    - Tăng `n_unanswerable`.
    - Chỉ tính đạt (`idk_ok += 1`) khi `"i don't know"` nằm trong `out["answer"].lower()` **và** `out["sources"] == []`; ngược lại thêm `(row["id"], "no_refusal")` vào `failures`.
  - Với câu trả lời được (`row["expected_source"] is not None`):
    - Tăng `n_answerable`.
    - `hit` đúng khi `row["expected_source"] in out["retrieved"]`; tăng `hits` nếu `hit`.
    - `facts` đúng khi `all(f.lower() in out["answer"].lower() for f in row["expected_facts"])`; tăng `facts_ok` nếu `facts`.
    - Nếu `not hit`, ghi `(row["id"], "retrieval_miss")` (kể cả khi câu trả lời vẫn chứa fact); ngược lại nếu `not facts`, ghi `(row["id"], "answer_miss")`.
  - Giữ `failures` đúng theo thứ tự trong `eval_set`.
- Trong `report_lines`:
  - Định dạng mỗi tỉ lệ thành `"n/a"` nếu mẫu số bằng `0`, hoặc `f"{num}/{den} ({round(num / den * 100)}%)"` nếu khác `0`.
  - Trả về danh sách các dòng đúng thứ tự: `"hit@k: ..."`, `"facts: ..."`, `"refusals: ..."`, mỗi lỗi một dòng `"FAIL <id>: <reason>"` theo thứ tự, và cuối cùng `"failures: <count>"`.
