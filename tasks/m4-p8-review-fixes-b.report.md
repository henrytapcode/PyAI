# Báo cáo M4 bước 25b (đợt b): sửa p8-04 và p8-05 theo review

## 1. Đã làm gì

### Quy ước `FakeClock` & đồng hồ chung (p8-04, p8-05)
- Thống nhất dùng `FakeClock` (thuộc tính `self.t`, `__call__() -> float`, `advance(seconds)`) tại mọi nơi trong `p8-04-monitoring` (lesson §1, `examples/01_request_log.py`) và `p8-05-mini-project` (lesson §2/§4/§5/§6, `examples/02`, `examples/03`, `ex02/test_exercise.py`).
- Đo độ trễ bằng `(clock() - start) * 1000` (ms), bỏ toàn bộ `now_ms` và `.now`.
- Ở `p8-04` §1, nhắc đây là `FakeClock` của `p8-03-caching` (gọi `clock()` được nhờ `__call__`), truyền `clock` vào `tracked_chat`, thêm giải thích `time.perf_counter` vs `time.monotonic` (m6), đổi `req-01`/`req-02` ở §2 sang `req-03`/`req-04` để tránh trùng id khác cost với §1 (m5), và dùng đơn giá `0.002`/`0.006` ở §1 + `01_request_log.py` để tránh in dạng khoa học `3.6e-05` (m5).
- Ở `p8-05` §2, nhắc ngắn gọn việc dùng lại `FakeClock` từ `p8-03-caching` nhờ `__call__` (M8).

### B1 + M2 + M5 + M3 + M4 + M8: `p8-05-mini-project`
- **Bài học (`lesson.en.md` / `lesson.vi.md`) & `meta.yaml`**:
  - Sửa `duration_min` thành `75` (m8).
  - Bảng §1: sửa cột "from lesson" của Part 1 thành `new here (app factory), p7-09-mini-project-rag` / `mới trong bài này (app factory), p7-09-mini-project-rag` (M8); ghi rõ `p50_ms` và `alerts` là của bản minh họa bài học, không mâu thuẫn với `/metrics` ở Bài tập 2 (cập nhật cả Recap).
  - §2 (Part 1): bỏ `"t": clock()` khỏi `/health` để khớp `{"status": "ok", "docs": ...}` (m8); sửa `"ta"` -> `"bạn"` ở dòng 38 VI (m12).
  - §3 (Part 2): dùng `zip(docs, doc_vecs, strict=True)` thống nhất và thêm 1 câu giải thích `strict=True` (M8).
  - §4 (Part 3): thêm 1 câu giải thích vì sao cache key chỉ cần `question` + `top_k` (model, mẫu prompt và `min_score` cố định trong một app; đổi chúng thì thêm vào key hoặc tăng `index_version`) (m7) và lưu ý `time.monotonic` không chạy lùi (m6).
  - §5 (Part 4): bỏ `"status": "ok"` gán cứng trong `records.append(...)`; thêm 1–2 câu nói rõ bản minh họa chưa bắt lỗi model và Bài tập 2 sẽ thêm nhánh `RateLimitError` → `503` ghi `status="error"`.
  - §6 (Part 5): chỉnh bảng mô tả test thành 5 dòng khớp 5 hàm test (m8).
  - §7 (Part 6): sửa "single-line `main.py`" / "một dòng nối dây" thành "`main.py` only needs a few wiring lines" / "chỉ cần vài dòng nối dây" (m8, m12).
  - §8 Mistake 4: nối thêm 1 câu liên hệ Bài tập 2 (`RateLimitError` → `503` với `status="error"`).
- **ex01 (`ex01-rag-service`)**:
  - Thêm `GET /documents/{doc_id}` (trả `{"id": ..., "text": ...}` hoặc `404` `{"detail": "document not found"}`).
  - Thêm `"scores"` vào phản hồi `/ask` (làm tròn 3 chữ số, cùng thứ tự `sources`; `[]` khi từ chối).
  - Nếu model trả về đúng `"I don't know based on the provided context."`, đặt `sources=[]` và `scores=[]`.
  - Tái cấu trúc bằng các hàm phụ (`_select_matches`, `_build_prompt`) giảm trùng lặp với bài học xuống `28%` (≤ 35%), longest copied run `0` (≤ 4).
  - Cập nhật `alternatives/01_class_numpy.py` (và `.en.md`/`.vi.md`), `starter.py`, `prompt.en.md`/`.vi.md`, `exercise.yaml` (hint 3 tầng).
  - Bổ sung test trong `test_exercise.py` cho `/documents/{doc_id}`, `scores`, model refusal (`FakeLLM(script=[...])`), và M5 (`min_score=0.0, top_k=3`, assert toàn bộ list `sources` không xếp theo alphabet, kiểm tra đủ `[1] `, `[2] `, `[3] ` kèm đúng nội dung chunk).
- **ex02 (`ex02-cache-metrics`)**:
  - Bắt `RateLimitError` khi `client.embed` (lúc `/ask`) hoặc `client.chat` lỗi: trả `503` `{"detail": "model busy, retry later"}`, không cache, vẫn ghi record với `status="error"`, `cost=0.0` và `latency_ms` đo bình thường; các request khác ghi `status="ok"`.
  - Thêm `"error_rate"` vào `GET /metrics` và hỗ trợ `GET /metrics?last=N` (`last >= 1`, `last=0` trả `422`), giữ đúng thứ tự khóa `requests`, `cache_hit_rate`, `error_rate`, `p95_ms`, `total_cost`.
  - Tái cấu trúc bằng các hàm phụ (`_digest_cache_key`, `_percentile_nearest_rank`, `_retrieve_hits`, `_summarize_window`) giảm trùng lặp với bài học xuống `20%` (≤ 35%), longest copied run `0` (≤ 4).
  - Cập nhật `alternatives/01_class_cache_metrics.py` (và `.en.md`/`.vi.md`), `starter.py`, `prompt.en.md`/`.vi.md`, `exercise.yaml` (sửa `§4`/`§5` đúng heading, hint 3 tầng không dùng tên ngoài starter).
  - Bổ sung test trong `test_exercise.py`: lỗi `RateLimitError` trên `chat` và `embed` (503, không cache, `error_rate == 0.5`), `?last=N` và `?last=0 -> 422`, M3 (`>= 20` request có độ trễ phân biệt sao cho `p95 != max`), M4 (từ chối crypto vẫn tính `requests == 1`, app dùng đơn giá `0.001`/`0.002`).
  - **Sửa theo Feedback vòng 1**: bổ sung 1–2 câu giới thiệu `Query` của `fastapi` trong phần Rules/Quy tắc của `prompt.en.md` và `prompt.vi.md` (dùng cho tham số truy vấn tương tự `Field` cho body, ví dụ `last: int | None = Query(default=None, ge=1)`, FastAPI tự trả `422` khi vi phạm). Không sửa file nào khác ngoài `prompt.en.md`, `prompt.vi.md` và báo cáo này.

### M1 + M6 + M7 + Minor: `p8-04-monitoring` và quiz/examples
- **M1 (`p8-04` §7 Mistake 4, `q16`, `f05`)**: khởi tạo `status = "error"` trước `try`, chỉ gán `"ok"` sau khi `chat()` thành công, minh họa bằng trường hợp `ValueError` (role không hợp lệ) vẫn được ghi `"error"`, cập nhật `q16` (`3 0.67`) và `f05`.
- **M6 (`p8-04` ex02 `test_exercise.py`)**: parametrize kiểm tra ranh giới đúng bằng ngưỡng (`p95_ms == max_p95_ms`, `total_cost == budget`, `error_rate == 0.05`) và vượt ngưỡng một chút; thêm test `total_cost` làm tròn 6 chữ số từ giá trị 7 chữ số thập phân (`0.000058`).
- **M7 (Hint 3 tầng & `p8-04` ex01)**: sửa prompt `p8-04 ex01` viết rule bằng lời không lộ blank; tách `test_empty_list_raises_value_error` và `test_invalid_percentile_raises_value_error`; viết lại hint 3 tầng đúng chuẩn ở cả 4 exercise (`p8-04` ex01/ex02, `p8-05` ex01/ex02).
- **Minor (`m1`–`m4`, `m11`)**:
  - Sửa số dòng trong cả 6 file `examples/*.en.md` / `.vi.md` của 2 bài cho khớp file `.py`.
  - Đồng bộ tiêu đề example VI theo mẫu p1-01 (`**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`), sửa câu VI ở `p8-04/examples/02` (`giữ nguyên không đổi`) và `p8-05/examples/02` (`bỏ qua luôn bước embed`).
  - `p8-04/examples/03_daily_budget.py`: thêm tham số `warn_ratio: float = 0.8` vào `check_alerts`, sửa dữ liệu để mọi `cache_hit=True` và `status="error"` có `cost_usd=0.0`.
  - `p8-04` l.171 (m4): sửa lý do output đắt là "sinh tuần tự từng token" và đổi "3×–4×" thành "vài lần".
  - `p8-04` Mistake 1: chèn dòng trống trước `# fixed:` / `# đã sửa:` để `check_lesson_comments.py` không hiểu nhầm là dòng stdout.
  - Quiz (m11): viết lại distractor vô lý thành hiểu nhầm thực tế ở `p8-04` `q03`, `q06`, `q12`, `q14` và `p8-05` `q01`; thêm đáp án `rank-1` ở `p8-04` `q09` và `95.0` ở `p8-05` `q06`; bỏ `vec[0]` gượng ở `p8-05` `q14` thay bằng kiểm tra ngưỡng `cosine(q_vec, d_vec) >= 0.2`.

---

## 2. File đã sửa

### `curriculum/phase-08-production/p8-04-monitoring/`
- `lesson.en.md`, `lesson.vi.md`
- `examples/01_request_log.py`, `examples/01_request_log.out`, `examples/01_request_log.en.md`, `examples/01_request_log.vi.md`
- `examples/02_latency_report.en.md`, `examples/02_latency_report.vi.md`
- `examples/03_daily_budget.py`, `examples/03_daily_budget.en.md`, `examples/03_daily_budget.vi.md`
- `exercises/ex01-percentile/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `test_exercise.py`
- `exercises/ex02-metrics-tracker/exercise.yaml`, `test_exercise.py`
- `quiz.yaml`

### `curriculum/phase-08-production/p8-05-mini-project/`
- `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
- `examples/01_service_basics.en.md`, `examples/01_service_basics.vi.md`
- `examples/02_cache_in_action.py`, `examples/02_cache_in_action.en.md`, `examples/02_cache_in_action.vi.md`
- `examples/03_metrics_dashboard.py`, `examples/03_metrics_dashboard.en.md`, `examples/03_metrics_dashboard.vi.md`
- `exercises/ex01-rag-service/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_class_numpy.py`, `alternatives/01_class_numpy.en.md`, `alternatives/01_class_numpy.vi.md`
- `exercises/ex02-cache-metrics/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_class_cache_metrics.py`, `alternatives/01_class_cache_metrics.en.md`, `alternatives/01_class_cache_metrics.vi.md`

### Báo cáo
- `tasks/m4-p8-review-fixes-b.report.md`

(`curriculum/glossary.yaml` không sửa vì các thuật ngữ liên quan đã có sẵn.)

---

## 3. Kết quả lệnh kiểm tra

| Kiểm tra | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-08-production/p8-04-monitoring` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python tools/validate.py --path curriculum/phase-08-production/p8-05-mini-project` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` |
| `uv run python -m pytest curriculum/phase-08-production -p no:warnings --tb=no` | `115 passed in 0.71s` |
| `EXERCISE_TARGET=starter uv run python -m pytest ...p8-04-monitoring ...p8-05-mini-project -p no:warnings --tb=no` | `56 failed in 0.46s` (100% test fail trên starter) |
| `uv run ruff check curriculum/phase-08-production` | `All checks passed!` |
| `PYTHONIOENCODING=utf-8 PYTHONPATH=packages/pyai_llm uv run python tasks/check_lesson_comments.py ...p8-04-monitoring ...p8-05-mini-project` | `comment mismatches: 0` |
| `PYTHONIOENCODING=utf-8 uv run python tasks/check_overlap.py ...p8-05-mini-project` | `ex01-rag-service`: `19/68 lines in lesson (28%), runs>=5: 0`; `ex02-cache-metrics`: `27/133 lines in lesson (20%), runs>=5: 0`; `longest copied run: 0` |
| Tìm `now_ms\|\.now\b` trong `p8-04-monitoring` và `p8-05-mini-project` | `0` kết quả |
| `git diff --numstat curriculum/glossary.yaml` | Trống (`0` dòng sửa/xóa) |
| Script kiểm độ dài MCQ | `p8-04`: `mcq 7 longest-unique 0`; `p8-05`: `mcq 8 longest-unique 0`; `violations: 0` |

### Bảng kết quả kiểm tra mutant

| Exercise | Mutant | Kết quả pytest |
|---|---|---|
| `p8-04` ex02 | `p95_ms >= max_p95_ms` thay vì `>` | `1 failed, 21 passed` |
| `p8-04` ex02 | `total_cost >= budget` thay vì `>` | `1 failed, 21 passed` |
| `p8-04` ex02 | `error_rate >= 0.05` thay vì `>` | `1 failed, 21 passed` |
| `p8-04` ex02 | Bỏ `round(total_cost, 6)` | `1 failed, 21 passed` |
| `p8-05` ex01 | Cố định `ranked[:2]` thay vì `ranked[:top_k]` | `1 failed, 11 passed` |
| `p8-05` ex01 | Sắp xếp `sources` theo alphabet (`sorted(...)`) | `1 failed, 11 passed` |
| `p8-05` ex01 | Đánh số `[1]` cho mọi dòng context | `2 failed, 10 passed` |
| `p8-05` ex02 | Dùng `max(...)` thay vì nearest-rank `p95` | `1 failed, 13 passed` |
| `p8-05` ex02 | Hardcode giá `0.0005` / `0.0015` | `1 failed, 13 passed` |
| `p8-05` ex02 | Bỏ qua không ghi record khi refusal | `1 failed, 13 passed` |

---

## 4. Điều còn chưa chắc

- Ở `p8-05` ex02, `FakeLLM(fail_times=1)` đếm chung cả `chat` và `embed` nên `create_app` sẽ tiêu thụ ngay lần lỗi đầu khi embed tài liệu lúc khởi động; do đó trong `test_exercise.py`, nhánh `RateLimitError` ở `/ask` được kiểm bằng hai spy wrapper (`FailFirstAskChatClient` dùng `FakeLLM(fail_times=1)` riêng cho `chat`, và `FailFirstAskEmbedClient` ném ở lần `embed` thứ 2). Điều này đúng với hướng dẫn trong spec, nhưng nếu học viên chỉ dùng trực tiếp `FakeLLM(fail_times=1)` mà không bọc, `create_app` sẽ ném `RateLimitError` trước khi app khởi tạo xong (trừ khi `pyai_llm.FakeLLM` tách riêng `fail_times` hoặc thêm tùy chọn sau).
- Các file `p8-05` được chỉnh sửa bằng công cụ ghi UTF-8 trên Windows có thể có CRLF; nếu repo quy định LF nghiêm ngặt, có thể cần chuẩn hóa trước khi commit.
