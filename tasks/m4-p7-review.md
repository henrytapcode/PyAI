# Review phase 7 (2 reviewer subagent Opus, 2026-11-16)

Đã chia làm 2 nửa: p7-01..05 và p7-06..10. Cả hai nửa: validate 0 lỗi; pytest 80 + 90 test xanh; mọi khối python có output khớp comment; MCQ không lộ đáp án qua độ dài; `review_by` 2027-05-01 hợp lệ.
Boss đã tự kiểm lại: A-B1 (`chunk_words` ở p7-05 chép nguyên từ bài học), A-m2 (thứ tự `.env`/`.gitignore`), B-B1 (`issue_refund(**args)` ở p7-06 §6).

## Nửa A: p7-01..p7-05
- **B1** Solution chép lesson: p7-02 ex01 (`validate` §, l.112-130), p7-05 ex01 (`chunk_words` l.40-54), p7-04 ex02 (`VectorStore` §2 + `delete` §4). Bản nhẹ hơn: p7-01 ex02, p7-02 ex02, p7-05 ex02.
- **B2** hint3 + hint2 ra gần đủ lời giải: p7-03 ex02, p7-05 ex02, p7-04 ex02, p7-01 ex02, p7-02 ex02. Bài fill điền sẵn blank: p7-02 ex01, p7-03 ex01, p7-01 ex01.
- **M1** `re.findall` chưa được dạy (p7-05 lesson l.217, 226, ex02, examples).
- **M2** `__post_init__` chưa được dạy (p7-01 examples/02, p7-02 l.158, 172, quiz).
- **M3** p7-05 l.28, 327 nói quá về overlap ("never sliced in half").
- **M4** p7-01 ex02: test `estimate_cost` không ép làm tròn (mutant qua 7/7).
- **M5** Distractor MCQ vô lý: p7-03 q01, q03; p7-04 q01, q07, q09, q10; p7-05 q08, q14.
- m1 Số dòng trong example .md lệch. m2 thứ tự `.env`/`.gitignore`. m3 temp=0 "gần như tất định". m4 `response_format` riêng của FakeLLM; Pydantic lax mode. m5 p7-02 ex02 luật "not a dict" là code chết. m6 `meta.get(key)==val` với None. m7 NOTE "mọi DB pre-filter". m8 ngưỡng cosine tùy model. m9 p7-05 l.331 văn `while` / code `range`. m10 tên `build_messages`, `Hit` vs dict. m11 hint1 p7-05 ex01 gọi "`chunking`"; hint3 p7-01 ex02 `RuntimeError` vs `ValueError`. m12 văn VI trong hint. m13 p7-04 mistake 1 `raise` rồi `except` ngay.

## Nửa B: p7-06..p7-10
- **B1** p7-06 §6 l.319-334: `issue_refund(**args)` cho model tự đặt `confirmed=True`, `max_amount` (đã chạy).
- **M1** p7-10 ex02: bỏ append assistant/tool vẫn qua 12/12 (đã chạy). Cần `_SpyClient`.
- **M2** p7-10: approve trả False vẫn ra `needs_approval`. Tách thành `rejected`.
- **M3** p7-08 ex01 `hit_rate` chép §3. Bản nhẹ hơn: p7-06 ex01, p7-08 ex02, p7-07 ex02.
- **M4** Hint: p7-10 ex02 hint2 có code; p7-10 ex01 hint3 có 4 chỗ `...`; p7-08 ex02 hint3 ~90%; p7-09 ex01, p7-10 ex01 hint2 có biểu thức.
- **M5** `copy.deepcopy` chưa được dạy (p7-10 ex01, q15).
- m1 p7-07 ex02 test không kiểm strip `""` (đã chạy). m2 p7-08 ex01 thiếu test k≤0 (đã chạy). m3 p7-09 ex01 thiếu test ValueError + spy embed. m4 budget kiểm sau chat, bỏ final đã trả tiền. m5 chỉ xử lý `tool_calls[0]`. m6 p7-06 l.36, 59 mô tả FakeLLM chưa đúng. m7 p7-06 examples/03 .md "model proposed user_confirmed". m8 tên metric faithful/grounded/idk/refusals. m9 p7-09 l.413-418, 541-546 `or ... if ... else`, regex lookbehind. m10 p7-08 §5 chưa gọi tên dev set. m11 VI p7-06 §3 "(5) in". m12 hint3 bài fill điền sẵn blank.
