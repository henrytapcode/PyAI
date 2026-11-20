# Báo cáo M5 bước 2b — `cap-01-ex01` (`ChatBot`)

## 1. Đã làm gì
- Tạo hoàn chỉnh bài tập `cap-01-ex01` tại `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/`:
  - `exercise.yaml`: khai báo `id: cap-01-ex01`, `kind: project`, `difficulty: 3`, `tags: [llm, rag]` (khớp `curriculum/topics.yaml`), không đặt `runner` (chạy Pyodide), kèm 3 hint tăng dần cho cả `en` và `vi` (hint 1 trỏ §3/§4 kèm ví dụ cụ thể, hint 2 kế hoạch 6 bước, hint 3 khung class có `...`).
  - `prompt.en.md` và `prompt.vi.md`: mô tả nhiệm vụ (nêu rõ các phần lesson chưa làm như ghim `system` prompt, gom trạng thái vào class, từ chối không gọi `chat`, lọc citation `[n]`, viết lại theo câu gốc), ví dụ hội thoại 3 lượt (hỏi thường → nối tiếp → ngoài FAQ), và đủ 7 quy tắc hợp đồng `ChatBot` (tiếng Việt dùng "bạn", không dùng "ta"/"chúng ta", giữ thuật ngữ tiếng Anh).
  - `starter.py`: cung cấp sẵn `REFUSAL`, `DEFAULT_SYSTEM`, `build_index` và `retrieve` (tự viết gọn, chia câu giống p7-09), và khung `ChatBot` (`__init__`, `ask`) có docstring, ví dụ, `# TODO` và `pass`/`return None` để import sạch và fail từng test.
  - `solution.py`: cài đặt đầy đủ `ChatBot` đúng 7 quy tắc hợp đồng (embed chunk 1 lần trong `__init__`, `history` riêng theo instance, strip + `ValueError` khi rỗng, viết lại từ câu `user` gốc nếu `<= 4` từ / từ đầu chữ thường là `"and"` / bắt đầu bằng `"what about "` hoặc `"how about "`, từ chối `REFUSAL` không gọi `client.chat` khi không có hit, gọi `client.chat` với `temperature=0.0`, lọc citation `1 <= n <= len(hits)` không trùng theo thứ tự xuất hiện và trả nguyên văn `answer`, lưu câu gốc + trả lời và cắt lượt cũ với `pop(0)` khi vượt `max_history_tokens` mà vẫn giữ `len(history) > 2` và ghim `system`).
  - `alternatives/01_functional_deque.py` (+ `.en.md`, `.vi.md`): tách `rewrite_followup`, `extract_citations`, `trim_history_deque` thành hàm thuần cấp module, dùng `collections.deque.popleft()` để cắt lịch sử và `pyai_llm.cosine()` thuần Python thay cho NumPy trong `retrieve`.
  - `test_exercise.py`: 11 hàm test (13 test case khi parametrize) dùng `SpyClient` bọc `FakeLLM(embed_dim=256)` và chỉ dùng tập con pytest cho phép của browser runner, phủ đủ toàn bộ 9 kịch bản bắt buộc ban đầu cộng 2 test bổ sung ở vòng 2 (`test_tiny_token_budget_keeps_latest_turn_pair` và `test_k_parameter_limits_retrieved_context_chunks`).
- Sửa điều kiện tiền tố ở `examples/01_follow_up_chat.py` và `examples/02_dialog_eval.py`: đổi `("what about", "and", "how about")` thành `("what about ", "and ", "how about ")`.
- Kiểm thử mutant (chạy ở thư mục tạm, không sửa file trong repo):
  - `M1_unpinned_system` (đưa `system` vào danh sách bị `pop(0)` khi vượt ngân sách): fail 2 test (`test_consecutive_followups_rewrite_from_original_user_question`, `test_trims_oldest_turns_within_token_budget_and_pins_system`).
  - `M2_call_chat_when_no_hits` (gọi `client.chat` cả khi không có hit): fail 1 test (`test_out_of_faq_refuses_without_calling_chat`).
  - `M3_keep_invalid_citations` (giữ citation ngoài biên `1..len(hits)`): fail 1 test (`test_invalid_and_duplicate_citations_are_filtered_preserving_order`).
  - `M4_rewrite_using_rewritten` (lưu `rewritten` vào `history` thay vì câu gốc): fail 1 test (`test_consecutive_followups_rewrite_from_original_user_question`).
  - `M5_len_history_gt_0` (vòng 2 — đổi `len(self.history) > 2` thành `> 0`): fail 1 test (`test_tiny_token_budget_keeps_latest_turn_pair`), `1 failed, 12 passed`.
  - `M6_hardcoded_k_3` (vòng 2 — bỏ qua `self.k`, truyền cứng `3` vào `retrieve`): fail 1 test (`test_k_parameter_limits_retrieved_context_chunks`), `1 failed, 12 passed`.

## 2. File đã sửa / tạo
- Tạo mới:
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/exercise.yaml`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/prompt.en.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/prompt.vi.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/starter.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/solution.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/test_exercise.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.en.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.vi.md`
  - `tasks/m5-cap01-ex01.report.md`
- Sửa:
  - `curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.py` (dòng `startswith`)
  - `curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.py` (dòng `startswith`)

## 3. Kết quả lệnh kiểm tra
Chạy sau lần chỉnh sửa code cuối cùng (vòng 2 chỉ sửa `test_exercise.py`):
- `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`:
  - Exit code `1`: `ERROR curriculum/capstones/cap-01-rag-chatbot: missing quiz.yaml` (lỗi duy nhất mong đợi trước bước 2e).
  - `0 warning(s)` (không có cảnh báo `"copied from lesson code"`).
  - Đã kiểm tra: `1 lessons, 6 markdown pairs, 3 examples, 20 lesson output blocks, 1 alternatives, 1 exercises` (cả pytest lẫn browser runner cho `starter`, `solution`, `alternatives`).
- `uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot -q`:
  - Exit code `0`: `13 passed` (gồm cả 2 test mới `test_tiny_token_budget_keeps_latest_turn_pair` và `test_k_parameter_limits_retrieved_context_chunks` pass với `solution.py`).
- `EXERCISE_TARGET=alternatives/01_functional_deque uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot -q`:
  - Exit code `0`: `13 passed` (cả 2 test mới pass với `alternatives/01_functional_deque.py`).
- `EXERCISE_TARGET=starter uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot -q`:
  - Exit code `1`: `13 failed` (`0 passed`; cả 2 test mới đều fail với `starter.py`).
- `uv run ruff check curriculum/capstones/cap-01-rag-chatbot`:
  - Exit code `0`: `All checks passed!`.
- Kiểm tra 3 file example với `PYTHONPATH=packages/pyai_llm uv run python -W error`:
  - `ok` cả 3 file (`01_follow_up_chat.py`, `02_dialog_eval.py`, `03_session_store.py`), khớp hoàn toàn với `.out`.
- `git status --short`: chỉ có 2 file example sửa đổi (`01_follow_up_chat.py`, `02_dialog_eval.py`), thư mục `exercises/` mới trong `cap-01-rag-chatbot`, và `tasks/` (ngoài `.hallmark/` có sẵn trước đó).

## 4. Điều còn chưa chắc
- Chưa có `quiz.yaml` ở capstone này (đúng theo phạm vi loại trừ của bước 2b, chờ bước 2e), nên `validate.py` vẫn báo 1 lỗi `missing quiz.yaml` cho tới khi bước 2e hoàn thành.
- Trong thực tế, nếu câu hỏi nối tiếp mở đầu bằng `"and,"` có dấu phẩy dính liền (không có khoảng trắng trước dấu phẩy), `words[0].lower()` sẽ là `"and,"` chứ không phải `"and"` — hành vi hiện tại bám sát mô tả "từ đầu (chữ thường) là `\"and\"`" trong spec.
