# M4 bước 7: bài p6-03 Hugging Face pipelines

## Mục tiêu
Viết bài `p6-03-huggingface` trong `curriculum/phase-06-deep-learning/`, đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI. Kèm hai chỉnh nhỏ trong tooling (mục "Tooling") để code transformers chạy offline và đủ thời gian trong validate.
- Bài có `runner: local`. Trong app, code chạy qua runner cục bộ: child process đã đặt `HF_HUB_OFFLINE=1` và `HF_HUB_DISABLE_PROGRESS_BARS=1`.
- Người học vừa xong p6-01 (tensor, autograd) và p6-02 (`nn.Module`, logits, `argmax(dim=1)`, `eval()` + `no_grad()`, `state_dict`). Phase 5 đã dạy precision/recall và việc đánh giá trên dữ liệu của mình.
- Ý chính: kỹ sư AI hiếm khi train từ đầu. Bạn lấy model đã train sẵn trên Hugging Face Hub, hiểu tokenizer → model → logits → nhãn, rồi kiểm xem model có hợp với dữ liệu của mình không.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-06-deep-learning/p6-02-training-loop/` (commit `6e192a8`).

## Model dùng trong bài
Chỉ dùng model `sentiment` đã ghim trong `tools/localrunner/models.py` (đã có trong cache máy này):
```python
REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"
```
- Mọi `from_pretrained(...)` truyền `revision=REV, local_files_only=True`.
- Với `pipeline(...)`: nạp `tokenizer` và `model` bằng `from_pretrained` như trên, rồi truyền object vào: `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)`. Không truyền tên repo vào `pipeline` (khó ép offline). Ngoại lệ duy nhất: khối "ba dòng" đầu tiên ở §1 nếu worker chứng minh được nó không gọi mạng (xem "Kiểm không gọi mạng"); nếu không chứng minh được thì §1 cũng nạp object như trên.
- Không dùng model nào khác, không tải thêm gì.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-06-deep-learning/p6-03-huggingface/` và mọi file bên trong. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (pretrained model, tokenizer, token, input_ids, attention_mask, softmax, Hugging Face Hub). Thuật ngữ nào đã có thì bỏ qua.
- `curriculum/topics.yaml`: chỉ **thêm** một dòng `huggingface:  { en: "Hugging Face", vi: "Hugging Face" }` ngay sau dòng `pytorch:`.
- `tools/validate.py` và `curriculum/conftest.py`: chỉ các thay đổi trong mục "Tooling".
- `tasks/m4-p6-03-huggingface.report.md`

## Không được đụng
- `apps/`, `tools/localrunner/`, `tools/pyrunner/`, `curriculum/syllabus.yaml`, phase 0–5, `p6-01-tensors`, `p6-02-training-loop`, `exams/`, `pyproject.toml`, `uv.lock`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server ở foreground.
- `meta.yaml` **không** có trường `runner`.

## Tooling (nhỏ, bắt buộc)
Boss đã đo trên máy này: nạp tokenizer khoảng 2,5 s; nạp model + `pipeline` khoảng 5 s khi cache đã ấm, tới 9–14 s khi cache nguội. Không có `HF_HUB_OFFLINE=1` thì transformers còn hỏi mạng, mất thêm khoảng 3,5 s. Hiện `run_python` trong validate có timeout 15 s và không đặt biến offline.
1. `tools/validate.py`:
   - Ở đầu file, sau phần import: `os.environ.setdefault(...)` cho `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `HF_HUB_DISABLE_PROGRESS_BARS=1`. Các biến này đi vào cả code chạy trong process (browser runner, tracer) lẫn subprocess của `run_python`.
   - Code của bài có `runner: local` chạy với timeout 60 s thay cho 15 s (example, quiz, và khối code trong lesson nếu validate chạy chúng bằng `run_python`). Truyền qua tham số, không đổi giá trị mặc định cho các bài khác.
2. `curriculum/conftest.py`: `os.environ.setdefault` cho đúng ba biến trên, cạnh dòng `MPLBACKEND`.
3. Không đổi gì khác. Ghi diff của hai file vào report.

## Quy tắc code phase 6 (bắt buộc)
Giữ toàn bộ mục "Quy tắc code phase 6" trong `tasks/m4-p6-01-tensors.md` và phần thêm trong `tasks/m4-p6-02-training-loop.md`. Thêm cho bài này:
- Nạp model đúng mục "Model dùng trong bài". Khi chạy model trực tiếp: `model.eval()` và `with torch.no_grad():`.
- Score in ra làm tròn **3** chữ số. Nhãn lấy từ `model.config.id2label`.
- **Ngân sách thời gian:**
  - mỗi khối nạp model phải chạy dưới 10 s khi cache đã ấm;
  - lesson có **tối đa 5** khối nạp model; khối chỉ nạp tokenizer không tính;
  - 3 example, mỗi cái nạp model nhiều nhất một lần;
  - câu quiz có code chỉ được nạp tokenizer, **không** nạp model; tối đa 4 câu như vậy, còn lại là code torch thuần hoặc câu không có code.
- **stderr phải rỗng** với mọi khối, example và câu quiz, vì app hiện stderr màu đỏ. Kiểm bằng cách chạy từng khối và xem stderr. Nếu transformers in cảnh báo hay log thì tìm cách tắt đúng chỗ (vd tham số đúng, hoặc `transformers.logging.set_verbosity_error()` kèm một câu giải thích trong bài), và ghi vào report.
- Dùng câu tiếng Anh làm input cho model (model chỉ hiểu tiếng Anh). Phần giải thích trong `lesson.vi.md` vẫn bằng tiếng Việt.

## Kiểm không gọi mạng
Chạy mọi khối, example và quiz một lần **không** có `HF_HUB_OFFLINE` nhưng chặn mạng bằng proxy giả (`HTTPS_PROXY=http://127.0.0.1:9`, `HTTP_PROXY=http://127.0.0.1:9`). Mọi thứ phải chạy được và ra cùng output. Ghi cách làm và kết quả vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): model nhận diện cảm xúc, dịch, tóm tắt… phần lớn đã có người train sẵn. Hugging Face Hub là "thư viện" model đó. Kỹ sư AI chọn model, chạy nó đúng cách, và kiểm xem nó có đúng với dữ liệu của mình không. Bài này đi từ ba dòng `pipeline` tới từng bước bên trong.

1. **Pipeline: model đã train sẵn trong vài dòng.**
   - Chạy `sentiment-analysis` trên 3 câu kiểu phản hồi của người dùng chatbot, in nhãn và score.
   - Model đã được tải **một lần** vào cache bằng `fetch_models.py`. Khối `bash` (không chạy) ghi lệnh `uv run python tools/localrunner/fetch_models.py`, và một câu: bài học chạy offline, không gọi mạng.
   - Một câu về ghim `revision`: model trên Hub có thể đổi, ghim commit để kết quả không đổi theo thời gian.
2. **Tokenizer: chữ thành số.**
   - `AutoTokenizer.from_pretrained(...)`, `tokenizer.tokenize(text)` (từ hiếm bị tách thành mảnh `##`), `tokenizer(text)["input_ids"]`, `convert_ids_to_tokens`, token đặc biệt `[CLS]` / `[SEP]`. Model này là bản uncased, nên chữ hoa thành chữ thường.
   - **Picture in text** (fence `text`, giống hệt nhau ở EN và VI): câu → tokens → ids, căn cột.
   - Batch nhiều câu: `padding=True`, `truncation=True`, `return_tensors="pt"`. In `tuple(batch["input_ids"].shape)` và `attention_mask` dạng list (1 là token thật, 0 là padding).
   - Đây là section mời bấm **Visualize** (khối chỉ có tokenizer, ngắn, dưới 600 step; worker tự kiểm bằng `tools/pyrunner/tracer.py`: `len(steps)`, `truncated`, và thời gian).
3. **Model: từ ids tới logits tới nhãn.**
   - `AutoModelForSequenceClassification.from_pretrained(...)`, `model.eval()`, `with torch.no_grad(): out = model(**batch)`. Một câu giải thích `**batch` (truyền dict thành các tham số có tên, phase 1–2).
   - `out.logits` shape `(N, 2)`, `torch.softmax(logits, dim=1)` cho xác suất (giới thiệu softmax một câu: biến logits thành các số dương cộng lại bằng 1), `argmax(dim=1)`, `model.config.id2label`.
   - In kết quả và cho thấy nó khớp với `pipeline` ở §1 (cùng nhãn, cùng score làm tròn).
   - **Mermaid** `flowchart LR` (≤ 7 node): text → tokenizer → input_ids + attention_mask → model → logits → softmax → label + score.
   - **Trace table** `| text | logit NEG | logit POS | P(POS) | label |` cho 3 câu, số khớp output thật.
4. **Pipeline hay tự làm từng bước?**
   - **Bảng so sánh** `| use pipeline | do it step by step |`: thử nhanh, demo / cần logits, xử lý batch theo ý mình, fine-tune (p6-04), đưa vào service (phase 8).
   - Callout `[!TIP]`: hai cách cho cùng kết quả, vì pipeline chỉ gói đúng ba bước của §2–§3.
5. **Model không biết điều nó chưa được dạy.**
   - Chạy model trên câu trung tính, câu mỉa mai, câu ngoài lĩnh vực (vd log lỗi kỹ thuật), câu tiếng Việt không dấu. In nhãn và score. Model này chỉ có hai nhãn, nên câu trung tính vẫn bị ép thành POSITIVE hoặc NEGATIVE, thường với score cao.
   - Ý chính: score cao không có nghĩa là đúng. Trước khi dùng model nào, đánh giá nó trên vài chục mẫu dữ liệu thật của bạn (nối với precision/recall ở phase 5). Đây là cầu sang p6-04: fine-tune khi model chưa hợp dữ liệu.
   - Callout `[!WARNING]`.
6. **Lỗi thường gặp** (VI: `## 6. Lỗi thường gặp`), chạy thật để lấy đúng output:
   - Quên `return_tensors="pt"` rồi đưa vào model → lỗi (lấy dòng cuối thông báo thật).
   - Batch nhiều câu dài ngắn khác nhau mà không có `padding=True` cùng `return_tensors="pt"` → `ValueError` (lấy thông báo thật, cắt bớt nếu dài).
   - Gọi `model(batch)` thay cho `model(**batch)` → lỗi (lấy thông báo thật). Nếu lỗi này không rõ ràng hoặc không lỗi thì thay bằng một lỗi thật khác và ghi vào report.
   - Coi score là độ tin cậy thật: không có lỗi in ra, giải thích ngắn và trỏ lại §5.
7. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 15–20 phút. `review_by: "2027-05-01"` (thư viện HF đổi nhanh). `tags: [huggingface, pytorch]` (có thể thêm `dl`). `prerequisites: [p6-02-training-loop]`. `further_reading`: Hugging Face LLM Course chương 2 "Using Transformers" (pipeline, tokenizer, model) và model card của model đã dùng (URL chính thức trên huggingface.co; mở thử để chắc URL còn sống). Mỗi link mở được thì ghi vào report.

## Examples (3)
- `01_feedback_triage`: 6 phản hồi của người dùng chatbot; phân loại bằng pipeline; in từng dòng `label score text` rồi đếm số NEGATIVE. Đây là việc "triage" thực tế.
- `02_tokens_and_lengths`: chỉ dùng tokenizer. Với 4 câu, in số token (không tính token đặc biệt), câu dài nhất, và shape batch khi `padding=True`. Thêm một câu dài với `truncation=True, max_length=8` để thấy bị cắt.
- `03_logits_by_hand`: tokenizer + model, tự tính softmax và nhãn cho 3 câu, rồi so với pipeline dùng cùng object và in `match: True`.

## Exercises (2)
Trong cả hai bài, `starter.py` **đã nạp sẵn** tokenizer (và model ở ex02) ở mức module, dùng đúng `REPO`/`REV`/`local_files_only=True`. Người học chỉ viết phần trong hàm. Như vậy test không nạp lại model mỗi lần.
- `ex01-count-tokens` (`kind: fill`): `count_tokens(texts: list[str]) -> list[int]` trả số token (không tính `[CLS]` / `[SEP]`) cho từng câu, kiểu `int` Python. Các ô `___` nằm trong thân hàm. 4–5 test:
  - số đúng cho vài câu biết trước;
  - chuỗi rỗng → `0`;
  - chữ hoa và chữ thường ra cùng số;
  - danh sách rỗng → `[]`;
  - kiểu phần tử là `int`.
- `ex02-triage-feedback` (`kind: code`), hai hàm:
  - `classify(texts: list[str]) -> list[tuple[str, float]]`: tự làm từng bước (tokenizer với padding và truncation, `no_grad`, softmax, argmax, `id2label`), trả `(label, round(score, 3))`, score là `float` Python. Không dùng `pipeline`.
  - `negatives(texts: list[str], threshold: float) -> list[str]`: các câu có nhãn `NEGATIVE` với score ≥ `threshold`, giữ thứ tự gốc.
  - 5–6 test:
    - nhãn đúng cho 2–3 câu rõ ràng;
    - score là `float` trong `[0, 1]`;
    - kết quả khớp `pipeline` dựng từ cùng tokenizer và model;
    - `negatives` lọc đúng theo ngưỡng;
    - danh sách rỗng → `[]` cho cả hai hàm (chú ý: tokenizer với list rỗng có thể lỗi, nên solution phải xử lý trường hợp này);
    - khi hàm trả `None`, thông báo dễ hiểu (như vòng 2 của p6-01).
  - Starter import được, fail **mọi** test.
  - `alternatives/01_pipeline.py`: `classify` bằng `pipeline` dựng từ cùng object. File `.md` nói khi nào cách này đủ (thử nhanh) và khi nào cần tự làm (cần logits, xử lý batch riêng).
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 để trống ít nhất 2–3 dòng thật sự.
- Thời gian `pytest` cho cả bài và thời gian chạy `/test` ước tính (đo bằng `runner.run_tests` gọi trực tiếp) ghi vào report; mỗi lần dưới 30 s.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `huggingface` (chính), có thể thêm `pytorch`.
- Tuân thủ ngân sách: tối đa 4 câu có code nạp tokenizer, không câu nào nạp model.
- Phải có câu về: `[CLS]` / `[SEP]`; `attention_mask`; softmax và argmax; vì sao ghim `revision`; score cao không có nghĩa là đúng.

## Tiêu chí hoàn thành (checklist)
1. [ ] Tooling đúng mục "Tooling"; validate toàn bộ vẫn chạy được (boss sẽ chạy lại).
2. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` có `phase: p6`, `order: 3`, `tags` gồm `huggingface`, `prerequisites: [p6-02-training-loop]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng), không có `runner`.
3. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
4. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt, chỉ khác comment; số dòng mermaid bằng nhau; fence `text` giống hệt.
5. [ ] Tuân thủ quy tắc code; ngân sách thời gian; stderr rỗng; "Kiểm không gọi mạng" đạt. Các lệnh grep bên dưới rỗng.
6. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter: phải là 0); solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu, vd "tokenizer (bộ tách chữ thành token)".
8. [ ] Report ghi: thời gian từng khối nạp model, thời gian `validate.py --path`, số step và thời gian của khối Visualize.
9. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-03-huggingface
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-06-deep-learning
uv run ruff check curriculum/phase-06-deep-learning
uv run ruff check tools/validate.py curriculum/conftest.py
grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]" curriculum/phase-06-deep-learning/p6-03-huggingface
grep -rln "tensor(" curriculum/phase-06-deep-learning --include=*.out
uv run python tools/build_content.py
git status --short
```
Mong đợi:
- validate 0 lỗi; pytest exit 0; ruff sạch trong `curriculum/phase-06-deep-learning`;
- `tools/validate.py` không thêm lỗi ruff so với trước (hiện có 30 lỗi cũ; ghi số trước và sau vào report);
- hai lệnh grep rỗng;
- thay đổi chỉ nằm trong các file được phép.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục "phase 6+"), `tasks/m4-p6-01-tensors.md` và `tasks/m4-p6-02-training-loop.md` (quy tắc), `tools/localrunner/models.py`, rồi bài `p6-02-training-loop`.
- transformers 5.23.0: API có thể khác trí nhớ của bạn. Đọc `help()` hoặc source trong `.venv` khi không chắc, và ghi vào report những gì khác.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `tmp_path`, và `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash.
- Mọi lệnh phải tự kết thúc. Không chạy server ở foreground.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi, pytest curriculum xanh, typecheck + build xanh, khối lesson chạy được khi chặn mạng bằng proxy giả; trong app qua runner cục bộ: khối §5 chạy 4,6 s, stderr rỗng, starter ex02 0/5, solution qua hết; đã commit `8f3e5e5`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
