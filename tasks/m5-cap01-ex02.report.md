# Báo cáo: `m5-cap01-ex02` — Capstone 1, Exercise 2 ("eval hội thoại + cổng hồi quy")

## 1. Đã làm gì
- Tạo hoàn chỉnh bài tập `cap-01-ex02` trong `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/` đúng theo hợp đồng và hướng dẫn của `docs/CONTENT_GUIDE.md`:
  - `exercise.yaml`: khai báo `id: cap-01-ex02`, `kind: project`, `difficulty: 3`, `tags: [evaluation, rag]`, tiêu đề EN/VI và 3 hint tăng dần cho mỗi ngôn ngữ (hint 1 trỏ §5 + ví dụ cụ thể; hint 2 kế hoạch đánh số; hint 3 khung code với chỗ trống `...`), không có trường `runner`.
  - `prompt.en.md` và `prompt.vi.md`: mô tả nhiệm vụ nêu rõ các điểm lesson §5 chưa làm (bot mới qua `make_bot()` cho từng dialog, thứ tự ưu tiên lý do lỗi, khóa `(dialog, turn)`, mục `new`, danh sách `failures`, cổng `gate_ok`), phần Example với 2 dialog ngắn cùng output mẫu của `run_dialog_eval` và `compare_to_baseline`, và phần Rules đầy đủ hợp đồng; văn phong VI dùng "bạn", đảm bảo parity EN/VI.
  - `starter.py`: hằng `REFUSAL`, 3 hàm đúng chữ ký kèm docstring + ví dụ + `# TODO` từng bước và `return None`, import sạch.
  - `solution.py`: cài đặt `score_turn` (đúng thứ tự ưu tiên `no_refusal`, `refused`, `wrong_source`, `missing_fact` so không phân biệt hoa thường), `run_dialog_eval` (gọi `make_bot()` đúng 1 lần mỗi dialog, trả list theo thứ tự dialog rồi lượt đếm từ 1), và `compare_to_baseline` (duyệt 1 lượt trên `current`, bắt `ValueError` khi `current` rỗng, giữ nguyên thứ tự `current`, tách `new` khỏi `fixed`/`broken`, tính `pass_rate` làm tròn 3 chữ số và `gate_ok = not broken and pass_rate >= min_pass_rate`); không chép khối 5 dòng từ lesson §5.
  - `alternatives/01_set_diff_eval.py` (+ `.en.md`, `.vi.md`): cách tiếp cận khác dùng dict comprehension theo khóa `(dialog, turn)` và phép toán tập hợp (`set`) để tính `fixed`, `broken`, `new`, sau đó sắp xếp lại theo thứ tự `current`, kèm bảng kiểm tra tuần tự trong `score_turn`.
  - `test_exercise.py`: 10 hàm test (13 test case khi bung parametrize), chỉ dùng tập con pytest được runner trình duyệt hỗ trợ (`assert`, `pytest.raises`, `pytest.mark.parametrize`), dùng 2 bot giả `ScriptedBot` và `MemoryBot` ngay trong file test để kiểm đầy đủ các yêu cầu và biên trong spec.

## 2. File đã sửa / tạo
Tất cả nằm đúng trong phạm vi cho phép:
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/exercise.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/prompt.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/prompt.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/starter.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/solution.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/test_exercise.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/alternatives/01_set_diff_eval.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/alternatives/01_set_diff_eval.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/alternatives/01_set_diff_eval.vi.md`
- `tasks/m5-cap01-ex02.report.md`

Không đụng vào lesson, examples, `ex01-chatbot`, `quiz.yaml` hay bất kỳ file dùng chung nào khác.

## 3. Kết quả lệnh kiểm tra

### Lệnh kiểm tra theo spec (chạy tại `D:\Proj\python-ai-platform`)
1. `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot` (exit code `1`):
   - `ERROR curriculum/capstones/cap-01-rag-chatbot: missing quiz.yaml`
   - `FAILED: 1 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 20 lesson output blocks, 2 alternatives, 2 exercises.`
   - Chỉ còn đúng lỗi `missing quiz.yaml` theo đúng kỳ vọng của mốc hiện tại; **0 cảnh báo**; kiểm tra trên cả pytest lẫn browser runner (`tools/pyrunner/runner.py`) cho `starter`, `solution` và `alternatives/01_set_diff_eval.py` đều đạt.
2. `uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot -q` (exit code `0`):
   - `26 passed` (`..........................`), gồm cả `ex01-chatbot` và `ex02-dialog-eval`.
3. `EXERCISE_TARGET=starter uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval -q` (exit code `1`):
   - `0 passed`, `13 failed` (`FFFFFFFFFFFFF`) — toàn bộ test fail trên `starter.py`.
4. `uv run ruff check curriculum/capstones/cap-01-rag-chatbot` (exit code `0`):
   - `All checks passed!`
5. `git status --short`:
   - Chỉ có thư mục mới `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/` và `tasks/` (cùng `.hallmark/` có sẵn từ trước trong working tree).

### Kiểm tra 5 mutant ở thư mục tạm (không sửa repo)
Chạy `pytest` trên bản sao trong `tempfile.TemporaryDirectory()`:
1. **Gọi `make_bot()` một lần cho mọi dialog**: `2 failed, 11 passed` (`test_run_dialog_eval_calls_make_bot_once_per_dialog_and_isolates_history`, `test_run_dialog_eval_preserves_order_and_one_based_turns` fail).
2. **Đảo thứ tự lý do (`missing_fact` trước `wrong_source`)**: `2 failed, 11 passed` (`test_score_turn_failure_reasons_and_priority[result3-turn3-wrong_source]`, `test_run_dialog_eval_preserves_order_and_one_based_turns` fail).
3. **Tính lượt `new` bị fail vào `broken`**: `1 failed, 12 passed` (`test_compare_to_baseline_tracks_fixed_broken_new_and_failures` fail).
4. **Dùng `>` thay `>=` ở ngưỡng `min_pass_rate`**: `1 failed, 12 passed` (`test_compare_to_baseline_gate_passes_at_exact_threshold_and_rounds_pass_rate` fail).
5. **Bỏ hạ chữ thường khi so `expected_facts`**: `1 failed, 12 passed` (`test_score_turn_case_insensitive_facts` fail).

## 4. Điều còn chưa chắc
- Giao diện web (trình duyệt Pyodide thật) không được chạy trực tiếp vì không chạy dev server theo yêu cầu; tuy nhiên `tools/validate.py` đã chạy `tools/pyrunner/runner.py` (cùng runner với trình duyệt) và xác nhận `starter` fail, `solution` và `alternatives/01_set_diff_eval.py` pass.
- `validate.py` vẫn thoát mã `1` với đúng 1 lỗi `missing quiz.yaml` ở cấp capstone vì `ex03` và `quiz.yaml` chưa được tạo ở bước này.
