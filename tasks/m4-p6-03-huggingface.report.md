# Báo cáo: M4 bước 7 — `p6-03-huggingface`

## 1. Đã làm gì

- **Tooling (`tools/validate.py`, `curriculum/conftest.py`)**:
  - Thêm `os.environ.setdefault` cho `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `HF_HUB_DISABLE_PROGRESS_BARS=1` ngay sau `MPLBACKEND=Agg`.
  - Thêm tham số `timeout: int = 15` vào `check_examples` và `check_questions` trong `tools/validate.py`, truyền `timeout=60` cho các bài có `runner: local` trong `syllabus.yaml` (giữ mặc định `15` cho mọi bài khác).
- **Curriculum metadata (`curriculum/topics.yaml`, `curriculum/glossary.yaml`)**:
  - Thêm `huggingface:  { en: "Hugging Face", vi: "Hugging Face" }` ngay sau `pytorch:` trong `curriculum/topics.yaml`.
  - Thêm 6 thuật ngữ mới vào `curriculum/glossary.yaml`: `Hugging Face Hub`, `pretrained model`, `tokenizer`, `input_ids`, `attention_mask`, `softmax` (bỏ qua `token` vì đã có sẵn ở dòng 1696).
- **Bài học `curriculum/phase-06-deep-learning/p6-03-huggingface/`**:
  - `meta.yaml`: `phase: p6`, `order: 3`, `duration_min: 18`, `review_by: "2027-05-01"`, không có `runner`, 2 link `further_reading` đã kiểm tra sống.
  - `lesson.en.md` / `lesson.vi.md`: mở đầu + 6 mục + Recap/Tóm tắt; gồm khối `bash` cho `fetch_models.py`, picture in text (`Chatbot logs!`), mermaid `flowchart LR` (7 node, cùng số dòng EN/VI), bảng trace 3 câu khớp output thật, bảng so sánh `pipeline` vs tự làm từng bước, callout `[!TIP]` và `[!WARNING]`, lời mời **Visualize** ở §2, và 4 lỗi thường gặp ở §6.
  - `examples/` (3): `01_feedback_triage`, `02_tokens_and_lengths`, `03_logits_by_hand` (kèm `.out`, `.en.md`, `.vi.md`).
  - `exercises/` (2):
    - `ex01-count-tokens` (`kind: fill`): 5 test, `starter.py` nạp sẵn `tokenizer`, fail 0/5.
    - `ex02-triage-feedback` (`kind: code`): `classify` + `negatives`, 5 test, `starter.py` nạp sẵn `tokenizer` và `model`, fail 0/5; kèm `alternatives/01_pipeline.py` (+ `.en.md`/`.vi.md`).
  - `quiz.yaml`: 16 câu (6 `mcq`, 4 `output`, 3 `fill`, 3 `parsons`; 5 dễ, 8 vừa, 3 khó) + 6 flashcard; tối đa 3 câu nạp `AutoTokenizer`, 0 câu nạp model, 0 câu `parsons` nạp `transformers`.

## 2. File đã sửa / tạo

**File sửa:**
- `tools/validate.py`
- `curriculum/conftest.py`
- `curriculum/topics.yaml`
- `curriculum/glossary.yaml`

**File tạo mới (`curriculum/phase-06-deep-learning/p6-03-huggingface/`):**
- `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
- `examples/01_feedback_triage.{py,out,en.md,vi.md}`
- `examples/02_tokens_and_lengths.{py,out,en.md,vi.md}`
- `examples/03_logits_by_hand.{py,out,en.md,vi.md}`
- `exercises/ex01-count-tokens/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `exercises/ex02-triage-feedback/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `exercises/ex02-triage-feedback/alternatives/01_pipeline.{py,en.md,vi.md}`
- `tasks/m4-p6-03-huggingface.report.md`

## 3. Diff của `tools/validate.py` và `curriculum/conftest.py`

```diff
diff --git a/curriculum/conftest.py b/curriculum/conftest.py
index 87afe78..9b1fc39 100644
--- a/curriculum/conftest.py
+++ b/curriculum/conftest.py
@@ -12,6 +12,9 @@ import pytest
 
 # Force non-interactive backend so matplotlib never opens GUI windows during pytest.
 os.environ.setdefault("MPLBACKEND", "Agg")
+os.environ.setdefault("HF_HUB_OFFLINE", "1")
+os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
+os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
 
 
 class ExerciseModule(pytest.Module):
diff --git a/tools/validate.py b/tools/validate.py
index 5609404..6b01bd6 100644
--- a/tools/validate.py
+++ b/tools/validate.py
@@ -42,6 +42,9 @@ from referencing.jsonschema import DRAFT202012
 
 # In-process tracer and browser runner run matplotlib code inside validate.py.
 os.environ.setdefault("MPLBACKEND", "Agg")
+os.environ.setdefault("HF_HUB_OFFLINE", "1")
+os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
+os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
 
 ROOT = Path(__file__).resolve().parent.parent
 CURRICULUM = ROOT / "curriculum"
@@ -216,7 +219,7 @@ def check_explained_code(rep: Report, py: Path, args, what: str) -> None:
     check_md_parity(rep, en, vi, args.allow_missing_vi)
 
 
-def check_examples(rep: Report, lesson_dir: Path, args) -> None:
+def check_examples(rep: Report, lesson_dir: Path, args, timeout: int = 15) -> None:
     ex_dir = lesson_dir / "examples"
     if not ex_dir.exists():
         rep.error(lesson_dir, "missing examples/ folder")
@@ -226,7 +229,7 @@ def check_examples(rep: Report, lesson_dir: Path, args) -> None:
         rep.error(ex_dir, "no example .py files")
     for py in files:
         out_file = py.with_suffix(".out")
-        code, out, err = run_python(py.read_text("utf-8"), cwd=ex_dir)
+        code, out, err = run_python(py.read_text("utf-8"), cwd=ex_dir, timeout=timeout)
         if code != 0:
             rep.error(py, f"example crashed:\n{err.strip()[-600:]}")
         elif not out_file.exists():
@@ -376,7 +379,13 @@ def check_missing_models(rep: Report, syllabus: dict, scope: Path) -> set[Path]:
 
 
 def check_questions(
-    rep: Report, path: Path, questions: list, ids: set, topics: set, skip_code: bool = False
+    rep: Report,
+    path: Path,
+    questions: list,
+    ids: set,
+    topics: set,
+    skip_code: bool = False,
+    timeout: int = 15,
 ) -> None:
     for q in questions:
         qid = q.get("id", "?")
@@ -396,7 +405,7 @@ def check_questions(
                     rep.error(path, f"{qid}: duplicate options in '{lang}'")
         code = q.get("code", "")
         if not skip_code and q["type"] == "output":
-            rc, out, err = run_python(code)
+            rc, out, err = run_python(code, timeout=timeout)
             if rc != 0:
                 rep.error(path, f"{qid}: code crashes: {err.strip()[-300:]}")
             elif norm_out(out) != norm_out(q["answer"]):
@@ -410,11 +419,11 @@ def check_questions(
                 for a in q["answer"]:
                     first = a[0] if isinstance(a, list) else a
                     filled = filled.replace("___", first, 1)
-                rc, _, err = run_python(filled)
+                rc, _, err = run_python(filled, timeout=timeout)
                 if rc != 0:
                     rep.error(path, f"{qid}: code with answers filled in crashes: {err.strip()[-300:]}")
         elif not skip_code and q["type"] == "parsons":
-            rc, _, err = run_python("\n".join(q["lines"]) + "\n")
+            rc, _, err = run_python("\n".join(q["lines"]) + "\n", timeout=timeout)
             if rc != 0:
                 rep.error(path, f"{qid}: parsons lines in given order crash: {err.strip()[-300:]}")
             if len(set(q["lines"])) != len(q["lines"]):
@@ -532,10 +541,12 @@ def main() -> int:
                 continue
             rep.count("lessons")
             skip_code = lesson_dir in skip_code_lessons
+            les_entry = lesson_index.get(meta["id"])
+            code_timeout = 60 if les_entry and les_entry[1].get("runner") == "local" else 15
             check_i18n_obj(rep, meta_path, meta, "", args.allow_missing_vi)
             check_md_parity(rep, lesson_dir / "lesson.en.md", lesson_dir / "lesson.vi.md", args.allow_missing_vi)
             if not skip_code:
-                check_examples(rep, lesson_dir, args)
+                check_examples(rep, lesson_dir, args, timeout=code_timeout)
             ex_root = lesson_dir / "exercises"
             ex_dirs = sorted(p for p in ex_root.iterdir() if p.is_dir()) if ex_root.exists() else []
             if not ex_dirs:
@@ -550,7 +561,13 @@ def main() -> int:
                 quiz = load_yaml(quiz_path)
                 if check_schema(rep, validators["quiz"], quiz, quiz_path):
                     check_questions(
-                        rep, quiz_path, quiz["questions"], ids, topics, skip_code=skip_code
+                        rep,
+                        quiz_path,
+                        quiz["questions"],
+                        ids,
+                        topics,
+                        skip_code=skip_code,
+                        timeout=code_timeout,
                     )
                     qs = quiz["questions"]
                     if len(qs) < QUIZ_MIN_QUESTIONS:
```

## 4. Ghi nhận về `transformers 5.23.0`, `stderr` và kiểm không gọi mạng

- **Hành vi `transformers 5.23.0` (`torch 2.15.0+cpu`, `huggingface_hub 2.4.0`)**:
  - Khi gọi `pipeline("sentiment-analysis", model=REPO, revision=REV)` mà **không** có `local_files_only=True` và không có `HF_HUB_OFFLINE=1`, thư viện gửi request tới `https://huggingface.co/api/models/.../additional_chat_templates` và retry 5 lần. Khi truyền `local_files_only=True` (kể cả trong `pipeline("sentiment-analysis", model=REPO, revision=REV, local_files_only=True)` ở §1), `pipeline` đọc `kwargs.get("local_files_only", False)` và truyền xuống `AutoConfig` / `AutoTokenizer` / `AutoModel` nên không gọi mạng.
  - Kiểm chứng thêm bằng cách monkeypatch `socket.create_connection` kết hợp `HTTPS_PROXY=http://127.0.0.1:9`, `HTTP_PROXY=http://127.0.0.1:9` và xóa `HF_HUB_OFFLINE`: khối §1 chạy thành công (0 kết nối socket).
  - Nếu chạy không có `HF_HUB_DISABLE_PROGRESS_BARS=1`, `from_pretrained` in thanh tiến trình `Loading weights: 100% ...` ra `stderr` (ngay cả khi bật `transformers.logging.set_verbosity_error()`). Khi có `HF_HUB_DISABLE_PROGRESS_BARS=1` (đã đặt sẵn trong `tools/localrunner/server.py`, `tools/validate.py`, `curriculum/conftest.py`), `stderr` rỗng hoàn toàn và `python -W error` sạch cảnh báo.
  - Trong §6, `model(batch)` (quên `**`) báo `TypeError: embedding(): argument 'indices' (position 2) must be Tensor, not BatchEncoding`.
- **Kiểm không gọi mạng (`HTTPS_PROXY=http://127.0.0.1:9`, `HTTP_PROXY=http://127.0.0.1:9`, không đặt `HF_HUB_OFFLINE` / `TRANSFORMERS_OFFLINE`, có `HF_HUB_DISABLE_PROGRESS_BARS=1`, chạy với `-W error`)**:
  - Tất cả 8 khối code trong `lesson.en.md`: `rc=0`, `stderr=''`, output khớp 100% với chế độ `HF_HUB_OFFLINE=1` và khớp comment `#`.
  - Tất cả 3 file `examples/*.py`: `rc=0`, `stderr=''`, output khớp `.out` (`01_feedback_triage.py`: `4.49s`, `02_tokens_and_lengths.py`: `2.48s`, `03_logits_by_hand.py`: `4.73s`).
  - Tất cả 10 câu quiz có code (`output`, `fill`, `parsons`): `rc=0`, `stderr=''`.
- **Link `further_reading` đã mở thử (HTTP `HEAD`)**:
  - `https://huggingface.co/learn/llm-course/chapter2/2` → `200 OK` (`Behind the pipeline · Hugging Face`)
  - `https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english` → `200 OK` (`distilbert/distilbert-base-uncased-finetuned-sst-2-english · Hugging Face`)

## 5. Số đo hiệu năng, Visualize, Exercise

- **Thời gian các khối code trong `lesson.en.md` (`HF_HUB_OFFLINE=1`, `-W error`)**:
  - Block 1 (§1 `pipeline` — nạp model #1): `5.03s` (`proxy: 5.47s`)
  - Block 2 (§2 tokenizer — khối Visualize, không nạp model): `2.51s` (`proxy: 2.52s`)
  - Block 3 (§2 batch padding, không nạp model): `2.61s` (`proxy: 2.51s`)
  - Block 4 (§3 `AutoModelForSequenceClassification` — nạp model #2): `5.01s` (`proxy: 4.87s`)
  - Block 5 (§5 `model` + `pipeline` — nạp model #3): `5.12s` (`proxy: 5.01s`)
  - Block 6 (§6.1 lỗi thiếu `return_tensors="pt"` — nạp model #4): `6.55s` (`proxy: 5.79s`)
  - Block 7 (§6.2 lỗi thiếu `padding=True`, chỉ nạp tokenizer): `2.68s` (`proxy: 2.79s`)
  - Block 8 (§6.3 lỗi `model(batch)` — nạp model #5): `4.79s` (`proxy: 4.60s`)
- **Khối Visualize (§2 Block 2, đo qua `tools/pyrunner/tracer.py`)**: `11` step, `truncated=False`, `error=None`, `2.53s`.
- **Exercises (`runner.run_tests` & `pytest`)**:
  - `ex01-count-tokens`: `starter.py` pass **0/5** (`0.01s`), `solution.py` pass **5/5** (`0.01s`).
  - `ex02-triage-feedback`: `starter.py` pass **0/5** (`1.77s`), `solution.py` pass **5/5** (`0.31s`), `alternatives/01_pipeline.py` pass **5/5** (`0.44s`).
  - `EXERCISE_TARGET=starter uv run python -m pytest curriculum/phase-06-deep-learning/p6-03-huggingface`: `10 failed in 4.37s` (**0/10** pass).

## 6. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-03-huggingface`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (tổng thời gian: `62.18s`).
- `uv run python tools/validate.py --fast`:
  `OK: 0 error(s), 0 warning(s). Checked 38 lessons, 293 markdown pairs, 112 examples, 76 exercises, 67 alternatives, 750 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-06-deep-learning`:
  `31 passed in 4.47s` (tổng thời gian lệnh `5.76s`, exit code `0`).
- `uv run ruff check curriculum/phase-06-deep-learning`:
  `All checks passed!` (exit code `0`).
- `uv run ruff check tools/validate.py curriculum/conftest.py`:
  Trước khi sửa: `30` lỗi trong `tools/validate.py`, `0` trong `curriculum/conftest.py`.
  Sau khi sửa: `30` lỗi trong `tools/validate.py` (không thêm lỗi mới), `0` trong `curriculum/conftest.py`.
- Lệnh grep (chạy qua Git Bash `C:\Program Files\Git\bin\bash.exe`):
  - `grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]" curriculum/phase-06-deep-learning/p6-03-huggingface` → rỗng (exit code `1`).
  - `grep -rln "tensor(" curriculum/phase-06-deep-learning --include="*.out"` → rỗng (exit code `1`).
- `uv run python tools/build_content.py`:
  `Built 38 lessons, 8 exams, 228 flashcards, 611 questions -> apps\web\src\generated` (exit code `0`).
- `git status --short`:
  `M curriculum/conftest.py`, `M curriculum/glossary.yaml`, `M curriculum/topics.yaml`, `M tools/validate.py`, `?? curriculum/phase-06-deep-learning/p6-03-huggingface/`, `?? tasks/` (và `.hallmark/` đã có từ trước).

## 7. Điều còn chưa chắc

- Chưa chạy `uv run python tools/validate.py` đầy đủ (không `--fast`) trên toàn bộ 38 bài; mới chạy `validate.py --path curriculum/phase-06-deep-learning/p6-03-huggingface` đầy đủ và `validate.py --fast` toàn repo.
- Chưa mở giao diện web để bấm Run/Visualize/Test trực tiếp qua `tools/localrunner/server.py` (do spec không cho chạy server hay `pnpm --filter web build`).
