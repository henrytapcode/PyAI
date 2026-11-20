# M5 bước 2a: capstone 1 "RAG chatbot có eval": syllabus, meta, lesson, examples

## Mục tiêu
Viết phần "bài" của capstone `cap-01-rag-chatbot` trong `curriculum/capstones/cap-01-rag-chatbot/`: `meta.yaml`, `lesson.en.md` + `lesson.vi.md`, 3 example (`.py`, `.out`, `.en.md`, `.vi.md`). Exercise và quiz làm ở bước sau (2b–2e).
Hạ tầng đã có (`29fffe3`, `7f46770`): build/validate coi thư mục này là bài, phase `cap`, id `cap-01-...`.

Capstone **không dạy lại** p7-09 (RAG FAQ bot) hay p8-05 (dịch vụ FastAPI + cache + metrics). Nó biến bot hỏi-đáp một lượt thành **chatbot nhiều lượt** có **bộ eval hội thoại** và **dịch vụ có phiên (session)**. Ba ý mới, mỗi ý một exercise sau này:
1. **Lịch sử hội thoại có ngân sách token** và **viết lại câu hỏi nối tiếp** ("What about express?") thành câu hỏi độc lập trước khi truy xuất.
2. **Eval theo hội thoại** (golden dialog, chấm từng lượt) và **so với baseline** để báo ca mới hỏng / mới sửa.
3. **Dịch vụ có session**: mỗi session giữ lịch sử riêng, hết hạn theo TTL với `FakeClock`, giới hạn số session.

## File được phép sửa/tạo
- `curriculum/syllabus.yaml`: **chỉ** mục `cap-01-rag-chatbot` trong `capstones:` (thêm `kind: project`, `outcomes` en/vi). Không thêm `runner` (bài chạy Pyodide; riêng ex03 sau này sẽ có `runner: local` ở mức exercise).
- `curriculum/capstones/cap-01-rag-chatbot/meta.yaml`, `lesson.en.md`, `lesson.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/01_*.py|.out|.en.md|.vi.md`, `02_*`, `03_*`
- `tasks/m5-cap01-lesson.report.md`

## Không được đụng
- Mọi file khác, kể cả `tools/**`, `apps/**`, `packages/**`, các phase, `portfolio.yaml` (bước 2e mới trỏ `lesson`).
- Không tạo `exercises/` hay `quiz.yaml` ở bước này.

## Việc cần làm

### 1. `meta.yaml`
`id: cap-01-rag-chatbot`, `phase: cap`, `order: 1`, `kind: project`, `level: applied`, `tags: [llm, rag, evaluation, production]`, `prerequisites: [p7-08-evals, p7-09-mini-project-rag, p8-05-mini-project]`, `duration_min: 90`, `review_by: "2027-05-01"`, title (giống syllabus), summary, 4 outcomes (en/vi, khớp syllabus), `further_reading` 1–2 mục có thật (giống dạng p7-09).

### 2. `lesson.en.md` (đọc khoảng 12–15 phút), theo `docs/CONTENT_GUIDE.md`
Giọng như p7-09: một "brief" thật từ người quản lý. Mở đầu không heading: vì sao bot một lượt chưa đủ (người dùng hỏi nối tiếp, cần đo chất lượng mỗi khi sửa, cần phục vụ nhiều người cùng lúc).
Các mục:
1. `## 1. The brief`: bot làm được gì, 3 user story, cùng kho FAQ 8 trang của p7-09 (chép **nguyên** danh sách `docs` từ p7-09 lesson §2 để dữ liệu khớp; được phép rút gọn nếu block quá dài nhưng phải ghi rõ là cùng dữ liệu).
2. `## 2. Architecture`: một mermaid (`flowchart LR`, ≤10 node) "user turn → rewrite → retrieve → answer + cite → history" và nhánh eval/service; bảng "part | what you build | reuse from" trỏ tới bài cũ (`p7-05`, `p7-08`, `p7-09`, `p8-03`, `p8-05`).
3. `## 3. Conversation history with a token budget`: ý tưởng → ví von → code nhỏ chạy được: lưu `history` là list các lượt `{"role", "content"}`, đếm bằng `count_tokens` của `pyai_llm`, bỏ lượt cũ nhất cho tới khi vừa ngân sách. Bảng trace (`| turn | tokens | kept |`).
4. `## 4. Follow-up questions`: vì sao "What about express?" truy xuất sai; quy tắc viết lại đơn giản, tất định, **không gọi LLM**: câu ngắn (≤ 4 từ) hoặc bắt đầu bằng "what about"/"and"/"how about" thì ghép với câu hỏi người dùng gần nhất. Code nhỏ + bảng so sánh điểm truy xuất trước/sau khi viết lại (dùng `client.embed` + `cosine`). Mời bấm **Visualize** ở một khối ngắn (< 600 bước).
5. `## 5. Evaluating conversations`: golden dialog = list lượt, mỗi lượt có `expected_source`, `expected_facts`, hoặc kỳ vọng từ chối. Chấm từng lượt, rồi so với baseline: `fixed` (trước fail, nay pass), `broken` (trước pass, nay fail). Code nhỏ trên dữ liệu giả (dict kết quả), không cần chạy cả bot.
6. `## 6. Sessions`: một dict `session_id → {"history", "last_seen"}`, hết hạn theo TTL với `FakeClock` chuẩn (chép đúng class trong CONTENT_GUIDE), và giới hạn số session (bỏ session lâu không dùng nhất). Code thuần Python, **không** import fastapi (bài chạy Pyodide). Nói rõ ex03 sẽ gói phần này sau các route FastAPI và chạy bằng runner cục bộ.
7. `## 7. Milestones`: bảng 3 mốc, mỗi mốc một exercise, kèm điều kiện "xong" đo được:
   - ex01 `ChatBot`: `ask(question)` trả `{"answer", "sources", "rewritten"}`; giữ lịch sử, viết lại câu nối tiếp, cắt lịch sử theo ngân sách, từ chối mà **không gọi chat** khi không chunk nào vượt `min_score`, chỉ giữ citation hợp lệ.
   - ex02 eval: `run_dialog_eval(make_bot, dialogs)` chấm từng lượt; `compare_to_baseline(current, baseline)` trả `fixed`, `broken`, `pass_rate`; cổng hồi quy fail khi có ca `broken` hoặc `pass_rate` dưới ngưỡng.
   - ex03 dịch vụ: `create_app(docs, client, clock, session_ttl, max_sessions)` với `POST /sessions`, `POST /sessions/{id}/messages`, `GET /sessions/{id}`; session hết hạn hoặc không có → 404.
   Mỗi mốc phải nêu ít nhất một yêu cầu mà code trong lesson **chưa** làm (quy ước "exercise không chép bài học"): ví dụ ex01 giữ nguyên system prompt khi cắt lịch sử; ex02 báo cả lượt nào của dialog nào; ex03 đếm `max_sessions` và trả 404 cho session hết hạn.
8. `## 8. Grading rubric`: bảng tiêu chí → cách đo → mức đạt (ví dụ: grounded 100% trên golden dialogs, refusal đúng 100%, không ca `broken`, test của 3 exercise xanh).
9. `## 9. Common mistakes` (2–4 lỗi thật, có code sai + output sai + cách sửa): ví dụ truy xuất bằng câu nối tiếp thô; cắt lịch sử làm mất system prompt; so baseline bằng `pass_rate` tổng mà bỏ qua ca `broken`; session dùng chung một list lịch sử (aliasing).
10. `## Recap` (4–6 bullet) và `## Take it further` (giống p7-09: một khối `bash` gọi API thật đọc key từ `.env`, không in key).

Quy tắc code trong lesson (áp mọi block `python`):
- Chạy độc lập được trong Pyodide, không mạng, không `input()`, không thời gian thật, không fastapi/torch.
- LLM chỉ qua `from pyai_llm import FakeLLM, count_tokens, cosine`. Đọc `docs/CONTENT_GUIDE.md` mục "Fake LLM client" để biết khi nào fake trả lời theo `Context:` (≥ 2 từ chung) và khi nào trả `"I don't know based on the provided context."`.
- Comment `# ...` ngay dưới `print(...)` là output và phải khớp output thật (validator kiểm). Comment giải thích đặt trước `print` hoặc cách một dòng trống.
- Không chép nguyên khối code dài từ p7-09/p8-05; dùng hàm nhỏ tự viết lại cho gọn.
- `python -W error` không cảnh báo.

### 3. `lesson.vi.md`
Dịch tự nhiên như giáo viên giỏi giảng, xưng "bạn" (không dùng "ta"/"chúng ta"), thuật ngữ giữ tiếng Anh (lần đầu có gloss), accuracy = "tỉ lệ đoán đúng". Code block giống hệt EN trừ comment; comment output **không** dịch. Mermaid cùng số dòng, chỉ dịch nhãn. Cùng heading số, cùng callout, cùng thứ tự. Heading VI: `## 9. Lỗi thường gặp`, `## Tóm tắt`, `## Mở rộng thêm` (xem p7-09 lesson.vi.md để giữ cách đặt tên).

### 4. Examples (3), theo mục Examples của CONTENT_GUIDE
- `01_follow_up_chat.py`: một cuộc hội thoại 4 lượt (có 1 câu nối tiếp, 1 câu không có trong FAQ) in từng lượt: câu hỏi, câu viết lại, nguồn, câu trả lời.
- `02_dialog_eval.py`: chấm 2 golden dialog và so với baseline, in bảng ngắn và danh sách `fixed`/`broken`.
- `03_session_store.py`: session store với `FakeClock`, TTL và giới hạn số session, in trạng thái sau mỗi bước.
Mỗi file dòng đầu là comment tóm tắt; `.out` đúng output; `.en.md`/`.vi.md` đúng khuôn (`# Title`, **What it shows**, **Step by step**, **Notice**, **Try it yourself**). Các example không được là lời giải của exercise sau này: chỉ minh họa, cố tình thiếu ít nhất một yêu cầu của mốc tương ứng (ghi rõ thiếu gì trong report).

## Tiêu chí hoàn thành (checklist)
- [ ] syllabus mục cap-01 có `kind: project` và outcomes khớp meta
- [ ] meta, lesson EN/VI, 3 example đủ file
- [ ] Lesson có ≥ 2 kiểu hình ảnh (mermaid, bảng trace, bảng so sánh), một lời mời Visualize
- [ ] Mục Milestones nêu đủ 3 exercise với điều kiện "xong" đo được và phần lesson chưa làm
- [ ] Validate chỉ còn 2 lỗi mong đợi: `lesson has no exercises` và `missing quiz.yaml` (không lỗi nào khác)
- [ ] grep "ta"/"chúng ta" trong `lesson.vi.md` và example `.vi.md` ra 0 dòng (trừ "người ta")

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot
for f in curriculum/capstones/cap-01-rag-chatbot/examples/*.py; do PYTHONPATH=packages/pyai_llm uv run python -W error "$f" | diff - "${f%.py}.out" && echo "ok $f"; done
grep -nE "(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) " curriculum/capstones/cap-01-rag-chatbot/*.vi.md curriculum/capstones/cap-01-rag-chatbot/examples/*.vi.md | grep -v "người ta"
uv run python tools/build_content.py
git status --short
```

## Ghi chú cho worker
- Không chạy server hay dev server.
- Đọc trước: `docs/CONTENT_GUIDE.md`, `curriculum/phase-07-llm/p7-09-mini-project-rag/` (lesson EN/VI, examples), `curriculum/phase-08-production/p8-05-mini-project/lesson.en.md` (cách viết mini-project), `packages/pyai_llm/pyai_llm.py`.
- Nếu validate báo lỗi khác hai lỗi mong đợi, sửa nội dung, không sửa tool.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate chỉ 2 lỗi mong đợi, 3 example khớp .out, VI không "ta", trang bài hiện đủ heading + mermaid; còn `startswith("and")` trong example 01, 02 → sửa ở bước 2b; chờ duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Bài đạt phần lớn tiêu chí. Chỉ sửa 3 điểm sau, cả EN và VI, giữ mọi thứ khác nguyên:
1. `lesson.en.md` §6 (~l.258–270), `open_session`: nếu `sid` đã có trong `sessions` thì hiện đang ghi đè `{"history": [], ...}` và **xóa sạch lịch sử** của phiên đang dùng. Sửa để chỉ tạo mới khi `sid` chưa có; nếu đã có thì chỉ cập nhật `last_seen`. Output của khối giữ nguyên nếu có thể; nếu đổi thì cập nhật comment output và câu "Notice" cho khớp. Cùng khối code trong `lesson.vi.md` (chỉ comment được khác).
2. §4 `rewrite_query` (~l.126): `low.startswith(("what about", "and", "how about"))` khớp nhầm câu bắt đầu bằng "android…", "andy…". Đổi thành kiểm theo từ: ví dụ `low.startswith(("what about ", "and ", "how about "))` hoặc so `low.split()[0] == "and"`. Nếu câu Recap/§7 mô tả quy tắc thì giữ khớp. Output không đổi.
3. `examples/03_session_store.vi.md`, mục **Lưu ý**: "`last_seen` của cô" → viết trung tính, ví dụ "`last_seen` của `"alice"`".
Sau khi sửa chạy lại đúng các lệnh kiểm tra trong spec.
