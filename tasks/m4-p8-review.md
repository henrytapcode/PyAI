# Review phase 8 (2 reviewer subagent Opus, 2026-11-16)

Chia 2 nửa: A = p8-01..03, B = p8-04..05. Cả hai: validate 0 lỗi, pytest xanh, starter fail đúng.

## Nửa B: p8-04, p8-05
Reviewer: validate 0 lỗi; pytest 39 passed; starter fail 39/39; 20 khối lesson + 6 example khớp output, `-W error` sạch; 29 mutant, 12 lọt.
Boss tự kiểm lại: M1 (đúng: `status = "ok"` gán trước, lỗi lạ bị ghi "ok"); B1 (lesson §3 và §5 có service gần hoàn chỉnh; trùng nguyên dòng với solution: ex01 24/50, ex02 35/97, phần còn lại khác tên biến nhưng cùng cấu trúc).

- **B1** p8-05: ex01/ex02 gần như chép lesson §3 (l.153-234) và §5 (l.369-505); §6 có sẵn test mẫu; hint 3 ex01 chỉ chừa 3 `...`. Sửa: đổi yêu cầu exercise để phải tự ghép (vd ex02 thêm `error_rate`/`status` khi `RateLimitError` → 503, `p50_ms`, `alerts` có ngưỡng tham số; ex01 thêm yêu cầu lesson không có), hoặc rút lesson về các mảnh rời.
- **M1** p8-04 l.382-413 (+ q16, f05): `try/except/finally` ghi lỗi lạ thành `"ok"`. Sửa: khởi tạo `status = "error"`, gán `"ok"` sau khi `chat` thành công.
- **M2** p8-05 không có nhánh lỗi: `"status": "ok"` cứng (l.461), `RateLimitError` → 500 không record, `/metrics` không có `error_rate`, mâu thuẫn mistake 4 (l.854, 879). Sửa: try/except → 503 + record `status="error"`, thêm `error_rate`, test `FakeLLM(fail_times=1)`.
- **M3** p8-05 ex02 test p95 chỉ 2 giá trị, mutant `max` lọt (đã chạy). Sửa: ≥ 20 request, p95 ≠ max.
- **M4** p8-05 ex02 thiếu test record cho refusal và giá tham số (2 mutant lọt). Sửa: test câu crypto → `requests == 1`; app giá 0.001/0.002.
- **M5** p8-05 ex01 test `top_k` yếu (`scored[:2]`, sources sắp alphabet, mọi dòng `[1]` đều lọt). Sửa: `min_score=0.0`, `top_k=3` → len 3; assert thứ tự đầy đủ; assert `"[2] "` trong context (spy).
- **M6** p8-04 ex02 không test ranh giới `>` (3 mutant `>=` lọt). Sửa: parametrize đúng ngưỡng.
- **M7** p8-04 ex01 fill: prompt l.11 (en/vi) lộ 3/4 blank, hint 2 lộ blank còn lại, hint 3 yếu hơn starter. Sửa: rules bằng lời, hint 3 khung 1 gap.
- **M8** p8-05 dùng chưa dạy: `__call__`, app factory (bảng l.24 ghi "builds on p8-01" sai), `zip(strict=True)`; FakeClock đổi giao diện qua 3 bài (`.now` / `.now_ms` / callable giây). Sửa: giải thích `__call__` hoặc `clock=lambda: fake.now`, sửa cột bảng, nói vì sao callable.
- m1 Số dòng trong example .md lệch (p8-05 cả 3, p8-04 02 và 03).
- m2 p8-04 examples/03 .en.md nhắc `warn_ratio` không có trong code; data cho cache hit / lỗi có cost khác 0, mâu thuẫn §1.
- m3 Lệch VI/EN: p8-04 02 "hầu như đứng yên"; p8-05 02 thiếu ý "skip embed"; "Bài này minh họa" → "Ví dụ này minh họa".
- m4 p8-04 l.171 lý do output đắt ("forward pass") → "sinh tuần tự từng token"; "3×-4×" → "thường vài lần".
- m5 p8-04 l.7 nói "inject" nhưng §1 dùng global `clock`; §1/§2 cùng `req-01` khác cost; `3.6e-05`.
- m6 `perf_counter` (p8-04) vs `monotonic` (p8-05): thêm 1 câu nối.
- m7 p8-05 §4 l.240: giải thích vì sao key chỉ question + `top_k` (model, prompt, `min_score` cố định trong app).
- m8 p8-05: `sources=[]` khi model trả "I don't know" (p7-09 có làm); `/health` §2 trả thêm `"t"`; bảng l.664-673 6 dòng cho 5 test; l.680 "single-line main.py" nói quá; `duration_min` 45 thấp cho 900 dòng.
- m9 Hint: p8-05 ex02 hint 3 dùng `_run_rag` không có trong starter; hint 1 "Parts 3 and 4" lệch số heading; p8-04 ex02 hint 1 không chỉ mục, hint 2 lộ logic, hint 3 gap quá lớn.
- m10 Test: p8-04 ex01 tên `test_empty_list_raises_value_error` kiểm cả p; p8-04 ex02 không kiểm `round(total_cost, 6)`.
- m11 Quiz: distractor vô lý p8-04 q03, q06, q12, q14; p8-05 q01. Fill p8-04 q09 thêm `rank-1`; p8-05 q06 thêm `95.0`. p8-05 q14 dòng `vec[0]` gượng.
- m12 VI: p8-05 l.38 trộn "ta"/"bạn"; l.680 "một dòng nối dây".

## Nửa A: p8-01..p8-03
Reviewer: validate 0 lỗi; pytest 44 passed; 25 khối lesson (EN+VI), 9 example, 27 câu quiz chạy `-W error`; mutant trong scratchpad.
Boss tự kiểm lại: B1 (đúng: dòng `good temp=0.8 #2` in ra không có "Here is what I know: ").

- **B1** p8-03 lesson.en/vi:475: comment output sai (`good #2` thật ra trùng `good #1`), mất ý "bỏ cache thì câu trả lời đa dạng". Sửa: chứng minh bằng đếm `real_calls` (sai 1, đúng 2), hoặc chạy lại rồi cập nhật comment. Validator không so comment output của khối lesson (đề xuất riêng, ngoài phạm vi sửa nội dung).
- **M1** p8-02 `.dockerignore` (lesson l.177-216, examples/03 + .out, f05): Docker khớp pattern từ gốc context, `*.pyc`/`__pycache__/` không bắt thư mục con; mô phỏng lại khớp mọi cấp như `.gitignore`. Sửa: dạy `**/__pycache__`, `**/*.pyc`; mô phỏng root-relative; ghi khác biệt với `.gitignore`.
- **M2** p8-03 l.277: "truyền `time.monotonic`" nhưng `TTLCache` gọi `self.clock.now` → AttributeError. Sửa: clock là callable (`FakeClock.__call__`) hoặc sửa câu. VI l.41 bỏ "hay đổi múi giờ".
- **M3** p8-01 ex02 test yếu (4 mutant lọt: bỏ `.lower()`, bỏ `ge=1`, bỏ `max_length`, so chuỗi con). Sửa: thêm `top_k=0`, `"a"*201`, query khác hoa thường.
- **M4** p8-02 ex02 linter test yếu (5 mutant lọt: TOKEN/SECRET, `ADD .env`, `:LATEST`, `RUN` bất kỳ, chỉ token đầu `ENV`). Sửa: thêm các case vào parametrize.
- **M5** p8-03 ex02 test yếu (3 mutant lọt: hết hạn không tăng `misses`, key bỏ params khác, key bỏ `role`). Sửa: assert `misses == 1`, `hit_rate() == 0.5`; test `max_tokens`, `role`.
- **M6** Hint lộ/không leo thang: p8-01 ex01 hint 1 nêu mọi blank, hint 3 chép starter; p8-02 ex01 (debug) starter TODO + prompt + hint 1 liệt kê đủ 4 lỗi; p8-01 ex02 hint 2 + 3 ghép ra lời giải; p8-03 ex01 hint 2 nêu blank, solution gần chép `LRUCache` §5.
- **M7** 6 file `examples/*.vi.md` của p8-02, p8-03 giữ tiêu đề tiếng Anh (`What it shows`, `Step by step`, `Notice`, `Try it yourself`). Sửa theo mẫu p1-01.
- m1 Số dòng trong example .md lệch (p8-01 01, 03; p8-02 01, 02; p8-03 cả 3).
- m2 p8-01: 02 .vi.md "bốn payload sai kiểu" → "không hợp lệ"; `/docs/{doc_id}` dễ nhầm trang `/docs` (l.76, q01, f02) → `/documents/{doc_id}`; ex01 thiếu test `GET /notes/1` thành công (mutant `float` lọt).
- m3 p8-02: ex01 `python:slim` qua, `--host=0.0.0.0` fail; l.116 "every instruction builds a layer"; l.229 nói quá về pin tag; l.177 build context gửi lúc bắt đầu build; `split(None, 1)`, `fnmatch`, `PurePosixPath` chưa giới thiệu.
- m4 p8-03: l.95 sha256 chưa giải thích; l.145 JSON thiếu dấu cách; l.63 p2-07 dạy `cache_results` tự viết, không phải `functools.cache`; l.206 lý do bỏ cache khi đổi model (key đã có model → lý do là RAM); VI "hàm thuần (pure function)", "tiêm" → "truyền vào (inject)"; examples/01 Try-it đổi temperature không có tác dụng; ex02 hint 3 dùng `{**m, ...}`.
- m5 Quiz: distractor vô lý p8-01 q03, p8-02 q01, p8-03 q13, q16; p8-02 q10 dòng lọc `.env` vô nghĩa; p8-02 q04 thêm `".env*"`.
