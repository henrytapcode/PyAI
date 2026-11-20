# M4 bước 4: tải model Hugging Face nhỏ cho p6-03, p6-04

## Mục tiêu
p6-03 (pipeline) và p6-04 (fine-tune nhỏ) cần model thật, nhưng bài học và test **không được gọi mạng** (CONTENT_GUIDE, mục phase 6+). Làm một danh sách model ghim phiên bản, một script tải **một lần** vào cache HF, và cách kiểm tra cache để validate báo lỗi dễ hiểu khi thiếu.

## File được phép sửa/tạo
- `tools/localrunner/models.py` (mới): danh sách model và hàm kiểm tra cache.
- `tools/localrunner/fetch_models.py` (mới): CLI tải model.
- `tools/localrunner/test_models.py` (mới)
- `tools/localrunner/README.md`: thêm mục "Models".
- `tools/validate.py`: chỉ thêm phần kiểm tra cache model (mục C).
- `tasks/m4-04-fetch-models.report.md`

## Không được đụng
- `curriculum/`, `apps/`, `tools/pyrunner/`, `tools/localrunner/server.py`, `tools/localrunner/child.py`, `pyproject.toml`, `uv.lock`. Không thêm thư viện; `huggingface_hub` đã có sẵn, đi kèm transformers.
- Không xóa file, không `git commit`, không chạy `pnpm --filter web build`, không chạy server hay dev server ở foreground.
- **Không commit model vào repo.** Model chỉ nằm trong cache HF mặc định của máy.

## A. `models.py`
```python
MODELS = [
    {
        "key": "sentiment",
        "repo_id": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        "revision": "<commit sha 40 ký tự>",
        "purpose": "p6-03: pipeline('sentiment-analysis') inference",
    },
    {
        "key": "tiny-bert",
        "repo_id": "prajjwal1/bert-tiny",
        "revision": "<commit sha 40 ký tự>",
        "purpose": "p6-04: fine-tune a tiny classifier on CPU",
    },
]
```
- `revision` là commit sha hiện tại của từng repo. Lấy bằng `huggingface_hub.HfApi().model_info(repo_id).sha` rồi **ghi cứng** vào file, để model không đổi theo thời gian.
- `allow_patterns` cho từng model: chỉ tải file cần cho PyTorch và tokenizer (`*.json`, `*.txt`, và `*.safetensors` nếu repo có, nếu không thì `pytorch_model.bin`). Không tải `tf_model.h5`, `flax_model.msgpack`, `*.onnx`, `rust_model.ot`, `coreml/*`, `onnx/*`.
- Hàm `model_path(key) -> str | None`: đường dẫn snapshot trong cache, hoặc `None` nếu thiếu. Dùng `huggingface_hub.snapshot_download(..., local_files_only=True)` trong try/except, **không** gọi mạng.
- Hàm `missing_models() -> list[str]`: các `key` còn thiếu.
- Lesson sẽ nạp model bằng `repo_id` và `revision` kèm `local_files_only=True`. Ghi một ví dụ trong docstring:
  `AutoModelForSequenceClassification.from_pretrained(REPO, revision=REV, local_files_only=True)`.

## B. `fetch_models.py`
- Lệnh: `uv run python tools/localrunner/fetch_models.py`.
  - Tải các model còn thiếu bằng `snapshot_download(repo_id, revision=..., allow_patterns=...)`.
  - In mỗi model trên một dòng: key, dung lượng đã tải (MB), đường dẫn.
  - Chạy lại khi đủ cả thì không tải gì, chỉ in "already cached".
- Thêm `--check`: không gọi mạng; in trạng thái từng model; thiếu thì exit code 1.
- Sau khi tải, tự kiểm offline: đặt `HF_HUB_OFFLINE=1`, nạp tokenizer và model của từng key bằng `local_files_only=True`, và với `sentiment` chạy `pipeline` trên một câu. Lỗi nào cũng in rõ rồi exit 1.

## C. `validate.py`
- Trước khi chạy các bài, tìm các bài có `runner: local` trong syllabus đã có thư mục bài (ready) mà file `.py` hoặc `.md` của bài đó chứa `repo_id` của một model trong `MODELS`.
- Nếu model đó thiếu trong cache: báo **một** lỗi rõ ràng cho mỗi model, kèm lệnh `uv run python tools/localrunner/fetch_models.py`, và **bỏ qua** việc chạy code của các bài cần model đó (khỏi sinh hàng chục lỗi khó hiểu).
- Hiện chưa có bài p6 nào nên phần này không chạy. Test ở mục D dùng thư mục giả.
- Import `models.py` theo cách không làm validate chậm hơn: không import transformers hay torch ở mức module.

## D. Test (`tools/localrunner/test_models.py`)
Các test tooling này được dùng mọi tính năng của pytest.
1. Mọi `revision` trong `MODELS` là chuỗi hex 40 ký tự; mọi `key` là duy nhất.
2. `missing_models()` trả đủ mọi key khi `HF_HUB_CACHE` trỏ vào một `tmp_path` rỗng (dùng `monkeypatch.setenv` cùng cách nào đó để huggingface_hub đọc lại biến môi trường, vd truyền `cache_dir`). Thêm tham số `cache_dir=None` vào `model_path` / `missing_models` nếu cần để test được.
3. `fetch_models.py --check` với cache rỗng: exit code 1, output có tên các key.
4. Phần validate mục C: một hàm thuần, vd `lessons_needing_models(lesson_dirs, models)`, test bằng thư mục giả trong `tmp_path`.
5. Với cache thật (bỏ qua bằng `pytest.mark.skipif` nếu thiếu):
   - nạp `sentiment` offline (đặt env `HF_HUB_OFFLINE=1`), chạy `pipeline` trên `["I love this course", "This is terrible"]`: nhãn lần lượt `POSITIVE`, `NEGATIVE`;
   - chạy hai lần cho ra cùng score (làm tròn 4 chữ số);
   - nạp `tiny-bert` bằng `AutoModelForSequenceClassification(..., num_labels=2)` offline, cho chạy forward một batch 2 câu ra logits shape `[2, 2]`. Nếu có cảnh báo "newly initialized" thì đó là bình thường: ghi vào report để bài p6-04 dặn người học, rồi bỏ qua cảnh báo trong test.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đã tải hai model thật vào cache; report ghi revision, dung lượng từng model, đường dẫn cache.
2. [ ] `--check` chạy offline; chạy lại `fetch_models.py` không tải thêm gì.
3. [ ] Tự kiểm offline đạt; test 1–5 pass (test 5 chạy thật, không bị skip).
4. [ ] validate có phần kiểm cache đúng mục C; `uv run python tools/validate.py --fast` vẫn 0 lỗi.
5. [ ] Report: thời gian nạp và chạy pipeline sentiment trên CPU (để biết khối code p6-03 có dưới 10 s không); các cảnh báo in ra khi nạp model (dùng `-W error` thử xem; cảnh báo nào không tắt được thì ghi rõ).
6. [ ] Lệnh kiểm tra xanh; `git status` chỉ có file được phép.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/localrunner/fetch_models.py
uv run python tools/localrunner/fetch_models.py --check
uv run python -m pytest tools/localrunner -q
uv run ruff check tools/localrunner
uv run python tools/validate.py --fast
git status --short
```

## Ghi chú cho worker
- `huggingface_hub` 2.4.0: đọc tài liệu bằng `help()` hoặc đọc source trong `.venv` nếu API khác với trí nhớ. Ví dụ `huggingface_hub.constants` không truy cập được dưới dạng thuộc tính.
- Mọi lệnh phải tự kết thúc; không chạy server ở foreground.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: 22 test, ruff không thêm lỗi, sentiment + google BERT-Tiny nạp offline với -W error, tokenizer hạ chữ thường, logits (2,2); đã commit `27ac77d`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã kiểm: 22 test pass, `--check` offline đúng, sentiment chạy offline với `-W error` ra `POSITIVE 0.9999 / NEGATIVE 0.9996`, validate đúng mục C. Sửa 3 điểm (được phép sửa thêm `tools/localrunner/server.py` và `tools/localrunner/test_server.py` cho điểm 2):

1. **Đổi model tí hon.** `prajjwal1/bert-tiny` không có `model_type` trong `config.json`, nên `AutoTokenizer` / `AutoModelForSequenceClassification` báo `ValueError: Unrecognized model`. Bài p6-04 cho người mới không nên phải dùng class riêng chỉ vì model.
   - Thay bằng `google/bert_uncased_L-2_H-128_A-2`: BERT-Tiny gốc của Google, cùng kích thước, config có `"model_type": "bert"`, có `model.safetensors`. Ghim `revision` bằng sha hiện tại (boss thấy `30b0a37ccaaa32f332884b96992754e246e48c5f`; tự kiểm lại). `allow_patterns`: `["*.json", "*.txt", "*.safetensors"]`.
   - Tải về, rồi kiểm offline: `AutoTokenizer.from_pretrained(...)` (repo không có `tokenizer_config.json`; xác nhận tokenizer có hạ chữ thường: `tok("Hello")` và `tok("hello")` ra cùng `input_ids`), `AutoModelForSequenceClassification.from_pretrained(..., num_labels=2)` → logits `[2, 2]`.
   - Cập nhật test 5, phần self-check của `fetch_models.py`, README và report.
   - Không xóa cache cũ của `prajjwal1/bert-tiny` (nằm ngoài repo; boss sẽ báo user).
2. **Thanh tiến trình "Loading weights"** của transformers in ra stderr, nên trong app sẽ thành rác ở panel output. Boss đã thử: biến môi trường `HF_HUB_DISABLE_PROGRESS_BARS=1` tắt được nó (`TRANSFORMERS_VERBOSITY=error` thì không).
   - Thêm `HF_HUB_DISABLE_PROGRESS_BARS=1` vào `_child_env()` trong `server.py`.
   - Thêm một assert vào test môi trường của child trong `test_server.py`.
3. **Ghi vào report số đo thời gian** (boss đã đo, tự đo lại để xác nhận):
   - `from transformers import pipeline` mất khoảng 6–9 s mỗi lần chạy, không chỉ lần đầu;
   - nếu import `AutoTokenizer` / `AutoModel...` thì import khoảng 2.6 s nhưng nạp model lại mất khoảng 6 s;
   - tổng cộng mỗi khối code có transformers mất khoảng 9 s.

   Boss sẽ dùng các số này để chỉnh ngân sách thời gian cho bài p6-03 và p6-04.

Chạy lại toàn bộ lệnh kiểm tra, cập nhật report (thêm mục "Vòng 2").
