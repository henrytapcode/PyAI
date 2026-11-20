# Báo cáo M4 bước 4: Fetch và kiểm tra cache model Hugging Face

## 1. Đã làm gì

- **`tools/localrunner/models.py`**:
  - Khai báo `MODELS` gồm 2 model ghim phiên bản (commit SHA 40 ký tự):
    - `sentiment`: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`, revision `714eb0fa89d2f80546fda750413ed43d93601a13`, `allow_patterns=["*.json", "*.txt", "*.safetensors"]`.
    - `tiny-bert`: `prajjwal1/bert-tiny`, revision `6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837`, `allow_patterns=["*.json", "*.txt", "pytorch_model.bin"]`.
  - Khai báo `IGNORE_PATTERNS = ["tf_model.h5", "flax_model.msgpack", "*.onnx", "rust_model.ot", "coreml/*", "onnx/*"]` để loại trừ các file không dùng cho PyTorch (bao gồm thư mục `onnx/` trong repo `sentiment` vốn cũng có file `.json`/`.txt`).
  - Viết `get_model(key)`, `resolve_cache_dir(cache_dir=None)` (đọc `HF_HUB_CACHE` / `HUGGINGFACE_HUB_CACHE` / `HF_HOME` tại thời điểm gọi để test bằng `monkeypatch.setenv` hoạt động dù `huggingface_hub.constants` đã import trước), `model_path(key, cache_dir=None)` (dùng `snapshot_download(..., local_files_only=True)` trong `try/except`), và `missing_models(cache_dir=None)`.
  - Không import `torch`, `transformers`, hay `huggingface_hub` ở mức module (`snapshot_download` được import lười bên trong `model_path`). Ghi ví dụ `AutoModelForSequenceClassification.from_pretrained(REPO, revision=REV, local_files_only=True)` trong docstring.

- **`tools/localrunner/fetch_models.py`**:
  - Tải các model còn thiếu bằng `snapshot_download` với `revision`, `allow_patterns`, `ignore_patterns`; in một dòng mỗi model gồm `key`, dung lượng (`MB`), đường dẫn snapshot. Khi đã có trong cache thì không tải lại và in `already cached`.
  - Hỗ trợ `--check`: kiểm tra offline qua `model_path()`, in trạng thái từng model, thiếu thì exit code `1`.
  - Tự kiểm offline sau khi tải trong subprocess mới với `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `local_files_only=True`: nạp tokenizer/model cho từng key và chạy `pipeline("sentiment-analysis", ...)` cho `sentiment`, forward batch cho `tiny-bert`.

- **`tools/validate.py`**:
  - Thêm hàm thuần `lessons_needing_models(lesson_dirs, models)` quét các file `.py` và `.md` trong thư mục bài để tìm `repo_id`.
  - Thêm `check_missing_models(rep, syllabus, scope)` gọi trước vòng lặp bài học trong `main()`: kiểm tra các bài có `runner: local` trong `syllabus.yaml` đã có thư mục bài trên đĩa (ready) và nằm trong `scope`; nếu thiếu model trong cache thì báo một lỗi cho mỗi model kèm lệnh `uv run python tools/localrunner/fetch_models.py` và bỏ qua việc chạy code (examples, exercises, quiz code) của các bài cần model đó.

- **`tools/localrunner/test_models.py`**:
  - Test 1: kiểm tra `key` duy nhất và `revision` đúng 40 ký tự hex.
  - Test 2: `missing_models()` và `model_path()` với `HF_HUB_CACHE` trỏ tới `tmp_path` rỗng.
  - Test 3: `fetch_models.py --check` với cache rỗng (cả subprocess CLI và gọi `fetch_models.main(["--check"])`) trả exit code `1` và in tên các `key`.
  - Test 4: `lessons_needing_models()` trên thư mục giả trong `tmp_path` (`.py`, `.md`, bài không dùng model, file non-`.py`/`.md`).
  - Test 5: chạy với cache thật (không bị skip) trong subprocess offline (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`) để vừa kiểm tra đúng điều kiện offline từ lúc khởi động tiến trình, vừa không đưa `torch` vào `sys.modules` của tiến trình pytest (tránh làm hỏng assertion `assert "torch" not in sys.modules` trong `test_server.py::test_health`). Kiểm tra `sentiment` cho nhãn `["POSITIVE", "NEGATIVE"]`, score lặp lại 2 lần khớp nhau ở 4 chữ số thập phân, và `tiny-bert` forward batch 2 câu ra logits shape `[2, 2]`.

- **`tools/localrunner/README.md`**:
  - Thêm mục `## Models` hướng dẫn lệnh tải và `--check`.

## 2. File đã sửa / tạo

- Tạo mới: `tools/localrunner/models.py`
- Tạo mới: `tools/localrunner/fetch_models.py`
- Tạo mới: `tools/localrunner/test_models.py`
- Tạo mới: `tasks/m4-04-fetch-models.report.md`
- Chỉnh sửa: `tools/localrunner/README.md`
- Chỉnh sửa: `tools/validate.py`

## 3. Thông tin model đã tải vào cache

| Key | Repo ID | Revision (SHA) | Dung lượng | Đường dẫn snapshot |
| --- | --- | --- | --- | --- |
| `sentiment` | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` | `714eb0fa89d2f80546fda750413ed43d93601a13` | `255.65 MB` | `C:\Users\Henry\.cache\huggingface\hub\models--distilbert--distilbert-base-uncased-finetuned-sst-2-english\snapshots\714eb0fa89d2f80546fda750413ed43d93601a13` |
| `tiny-bert` | `prajjwal1/bert-tiny` | `6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837` | `17.15 MB` | `C:\Users\Henry\.cache\huggingface\hub\models--prajjwal1--bert-tiny\snapshots\6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837` |

## 4. Benchmark CPU & ghi chú cảnh báo cho bài p6-03, p6-04

- **Thời gian nạp và chạy `sentiment` pipeline trên CPU** (tiến trình Python lạnh, offline):
  - Lần đo 1: `import: 9.49s, load: 0.50s, infer: 0.04s, total: 10.03s`.
  - Lần đo 2 (với `-W error`): `import: 8.66s, load: 0.40s, infer: 0.04s, total: 9.10s`.
  - Nhận xét: thời gian load model + chạy inference chỉ mất ~`0.44s - 0.54s`, phần lớn thời gian (~`8.7s - 9.5s`) nằm ở import `transformers`/`torch`. Tổng thời gian chạy một script độc lập nằm sát ngưỡng 10s (9.1s–10.0s tùy page cache); timeout mặc định của localrunner (`RUN_TIMEOUT_S = 120`) dư sức đáp ứng.
- **Lưu ý quan trọng khi nạp `prajjwal1/bert-tiny` (cho bài `p6-04`)**:
  - `config.json` của `prajjwal1/bert-tiny` chỉ có các tham số kiến trúc (`hidden_size`, `num_hidden_layers`, ...), **không có khóa `model_type`**, và repo cũng **không có `tokenizer_config.json`**.
  - Với `transformers==5.23.0`, gọi trực tiếp `AutoTokenizer.from_pretrained("prajjwal1/bert-tiny", ...)` sẽ lỗi `ValueError: Couldn't instantiate the backend tokenizer...`, và gọi `AutoModelForSequenceClassification.from_pretrained("prajjwal1/bert-tiny", ...)` (không truyền `config`) sẽ lỗi `ValueError: Unrecognized model in prajjwal1/bert-tiny. Should have a model_type key in its config.json.`
  - Cách nạp chạy được offline: dùng `BertTokenizer.from_pretrained(repo, revision=rev, local_files_only=True)` và `BertForSequenceClassification.from_pretrained(...)` hoặc truyền `config=BertConfig.from_pretrained(repo, revision=rev, num_labels=2, local_files_only=True)` vào `AutoModelForSequenceClassification.from_pretrained(...)`.
- **Cảnh báo (`-W error`)**:
  - Khi chạy nạp và inference cả hai model offline với `python -W error`, lệnh thoát `0`: không có Python `warnings.warn` nào được phát sinh khi đọc từ cache (`local_files_only=True`).
  - Lần tải đầu tiên trên Windows (không bật Developer Mode) có `UserWarning` từ `huggingface_hub` về symlink cache (chỉ xuất hiện khi tải, không xuất hiện khi chạy offline; tắt được bằng `HF_HUB_DISABLE_SYMLINKS_WARNING=1`).
  - Khi nạp `tiny-bert` vào `*ForSequenceClassification`, `transformers` in ra `LOAD REPORT` qua logger (không phải Python warning nên `-W error` không chặn): liệt kê các trọng số MLM/NSP (`cls.*`) là `UNEXPECTED` và `classifier.weight`, `classifier.bias` là `MISSING` ("those params were newly initialized because missing from the checkpoint"). Bài `p6-04` cần dặn người học đây là bình thường vì checkpoint gốc chỉ pre-train masked LM, đầu phân loại 2 lớp mới khởi tạo sẽ được fine-tune. Ngoài ra có thanh tiến trình `Loading weights:` (tqdm) ghi ra stderr.

## 5. Kết quả các lệnh kiểm tra

| Lệnh | Kết quả |
| --- | --- |
| `uv run python tools/localrunner/fetch_models.py` (lần đầu tải) | Tải xong `sentiment` (255.65 MB) và `tiny-bert` (17.15 MB); khi đó tự kiểm offline thất bại ở `AutoTokenizer` của `tiny-bert` do thiếu `tokenizer_config.json` (đã sửa dùng `BertTokenizer` + `BertForSequenceClassification`). |
| `uv run python tools/localrunner/fetch_models.py` (chạy lại sau khi sửa) | Exit `0`; in `already cached` cho cả 2 model, không tải lại; `offline-check sentiment: POSITIVE (0.9997)`, `offline-check tiny-bert: logits (1, 2)`. |
| `uv run python tools/localrunner/fetch_models.py --check` | Exit `0`; in trạng thái `cached` và đường dẫn cho cả `sentiment` và `tiny-bert`. |
| `uv run python -m pytest tools/localrunner -q -rs` | Exit `0`; `22 passed` (test 5 chạy thật với cache, không bị skip). |
| `uv run ruff check tools/localrunner` | Exit `0`; `All checks passed!`. |
| `uv run python tools/validate.py --fast` | Exit `0`; `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `git status --short` | `M tools/localrunner/README.md`, `M tools/validate.py`, `?? .hallmark/` (có sẵn từ trước), `?? tasks/`, `?? tools/localrunner/fetch_models.py`, `?? tools/localrunner/models.py`, `?? tools/localrunner/test_models.py`. |

## 6. Điều còn chưa chắc

- **Tích hợp end-to-end phần C trong `validate.py` trên bài `p6` thật**: Hiện chưa có thư mục bài `p6-*` nào trong `curriculum/`, nên `check_missing_models()` mới được kiểm tra gián tiếp (trả tập rỗng trên curriculum hiện tại; hàm `lessons_needing_models()` được unit test bằng `tmp_path`). Luồng bỏ qua bài khi thiếu model ở `main()` của `validate.py` chưa chạy trên bài `p6` thật.
- **Thời gian import lạnh dưới 10s**: Tổng thời gian import `transformers` + `torch` + load + chạy pipeline `sentiment` đo được là `9.10s - 10.03s` trên máy này; nếu máy người học có ổ HDD chậm hoặc chưa warm cache OS, tổng thời gian khởi động tiến trình mới có thể vượt 10s (mặc dù bản thân load + inference chỉ mất ~`0.5s`).
- **`ruff check tools/validate.py`**: Không chạy trong danh sách lệnh spec, khi chạy thử trước đó `tools/validate.py` có sẵn 31 cảnh báo pre-existing ngoài phạm vi sửa; các dòng mới thêm đã được căn <= 100 ký tự nhưng chưa chạy `ruff` riêng cho chỉ phần diff.

---

## Vòng 2

### 1. Sửa theo feedback vòng 1

1. **Đổi model `tiny-bert` sang `google/bert_uncased_L-2_H-128_A-2`**:
   - `tools/localrunner/models.py`: cập nhật `tiny-bert` dùng `repo_id = "google/bert_uncased_L-2_H-128_A-2"`, `revision = "30b0a37ccaaa32f332884b96992754e246e48c5f"` (xác minh từ `HfApi().model_info()`), và `allow_patterns = ["*.json", "*.txt", "*.safetensors"]` (repo có `config.json` với `"model_type": "bert"`, `vocab.txt`, `model.safetensors`).
   - `tools/localrunner/fetch_models.py`: cập nhật `_OFFLINE_CHECK_CODE` dùng chung `AutoTokenizer` và `AutoModelForSequenceClassification` (bỏ `BertTokenizer`/`BertForSequenceClassification`), xác minh hạ chữ thường (`tok("Hello")["input_ids"] == tok("hello")["input_ids"]`), và chạy batch 2 câu ra logits shape `(2, 2)`.
   - `tools/localrunner/test_models.py`: cập nhật `test_cached_models_offline_inference` dùng `AutoTokenizer.from_pretrained` và `AutoModelForSequenceClassification.from_pretrained(..., num_labels=2)`, kiểm tra thêm `tiny_lowercase_ok` (`"Hello"` và `"hello"` ra cùng `input_ids`) và `logits_shape == [2, 2]`.
   - `tools/localrunner/README.md`: liệt kê 2 model đã ghim (`sentiment`, `tiny-bert`: `google/bert_uncased_L-2_H-128_A-2`) và cập nhật mô tả biến môi trường child (`HF_HUB_DISABLE_PROGRESS_BARS=1`).
   - Không xóa cache cũ của `prajjwal1/bert-tiny`.

2. **Tắt thanh tiến trình `Loading weights` ở child process**:
   - `tools/localrunner/server.py`: thêm `env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"` vào `_child_env()`.
   - `tools/localrunner/test_server.py`: thêm assert kiểm tra `os.environ.get("HF_HUB_DISABLE_PROGRESS_BARS") == "1"` trong `test_child_env_and_isolated_cwd`.

### 2. Thông tin model `tiny-bert` mới trong cache

| Key | Repo ID | Revision (SHA) | Dung lượng | Đường dẫn snapshot |
| --- | --- | --- | --- | --- |
| `tiny-bert` | `google/bert_uncased_L-2_H-128_A-2` | `30b0a37ccaaa32f332884b96992754e246e48c5f` | `17.14 MB` | `C:\Users\Henry\.cache\huggingface\hub\models--google--bert_uncased_L-2_H-128_A-2\snapshots\30b0a37ccaaa32f332884b96992754e246e48c5f` |

### 3. Số đo thời gian & cảnh báo (tiến trình Python lạnh, offline, CPU, `-W error`, `HF_HUB_DISABLE_PROGRESS_BARS=1`)

| Kịch bản | Import | Load model/tokenizer | Inference | Tổng | Ghi chú stderr |
| --- | --- | --- | --- | --- | --- |
| `from transformers import pipeline` (lần 1) | `7.72s` | `0.34s` | `0.03s` | `8.09s` | Trống (không warning, không progress bar) |
| `from transformers import pipeline` (lần 2) | `7.58s` | `0.29s` | `0.03s` | `7.91s` | Trống (xác nhận import `pipeline` mất ~7.6–7.7s mỗi lần chạy) |
| `AutoTokenizer` + `AutoModelForSequenceClassification` (`sentiment`) | `2.88s` | `6.72s` | `0.02s` | `9.63s` | Trống |
| `AutoTokenizer` + `AutoModelForSequenceClassification` (`tiny-bert`, `num_labels=2`) | `2.87s` | `6.39s` | `0.01s` | `9.27s` | Chỉ còn bảng `LOAD REPORT` (`cls.*` `UNEXPECTED`, `classifier.bias`/`weight` `MISSING`); không còn `Loading weights:` progress bar |

- Xác nhận nhận xét cho ngân sách thời gian bài `p6-03`, `p6-04`:
  - `from transformers import pipeline` kéo theo import nặng ngay lúc `import` (~`7.6–7.7s` trên máy đo, ~6–9s) ở mọi lần chạy; tổng với load + infer khoảng `8s`.
  - `from transformers import AutoTokenizer, AutoModelForSequenceClassification` import nhanh hơn (~`2.87–2.88s`), nhưng chuyển phần nạp backend sang lần gọi `from_pretrained` đầu tiên (~`6.39–6.72s`), nên tổng mỗi khối code có `transformers` vẫn khoảng `9.3–9.6s`.
  - Không có `UserWarning` hay Python warning nào khi nạp cả hai model offline với `-W error`.
  - Với `google/bert_uncased_L-2_H-128_A-2`, dù repo không có `tokenizer_config.json`, `AutoTokenizer.from_pretrained(..., local_files_only=True)` hoạt động bình thường và hạ chữ thường (`"Hello"` và `"hello"` ra cùng `input_ids`).

### 4. Kết quả lệnh kiểm tra (Vòng 2)

| Lệnh | Kết quả |
| --- | --- |
| `uv run python tools/localrunner/fetch_models.py` (lần tải `tiny-bert` mới) | Exit `0`; `sentiment: already cached (255.65 MB)`, tải `tiny-bert: 17.14 MB`, `offline-check sentiment: POSITIVE (0.9997)`, `offline-check tiny-bert: logits (2, 2)`. |
| `uv run python tools/localrunner/fetch_models.py` (chạy lại) | Exit `0`; `already cached` cho cả 2 model, tự kiểm offline đạt. |
| `uv run python tools/localrunner/fetch_models.py --check` | Exit `0`; `sentiment: cached (255.65 MB)`, `tiny-bert: cached (17.14 MB)`. |
| `uv run python -m pytest tools/localrunner -q -rs` | Exit `0`; `22 passed` (test 5 chạy thật với cache, không bị skip). |
| `uv run ruff check tools/localrunner` | Exit `0`; `All checks passed!`. |
| `uv run python tools/validate.py --fast` | Exit `0`; `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `git status --short` | `M tools/localrunner/README.md`, `M tools/localrunner/server.py`, `M tools/localrunner/test_server.py`, `M tools/validate.py`, `?? .hallmark/`, `?? tasks/`, `?? tools/localrunner/fetch_models.py`, `?? tools/localrunner/models.py`, `?? tools/localrunner/test_models.py`. |
