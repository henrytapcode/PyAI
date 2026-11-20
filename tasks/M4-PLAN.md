# M4: phase 6–8 + runner cục bộ (kế hoạch, 2026-11-14)

Nguồn: `docs/DESIGN.md` §3, §5, §10 (M4 = phase 6–8, runner cục bộ, AI tutor tùy chọn). Template bài: `docs/CONTENT_GUIDE.md`.
Quy trình như M3: `/delegate` (boss viết spec `tasks/<slug>.md`, Gemini làm, boss chạy lại cổng và xem trong app), mỗi bước một commit sau khi user duyệt.
Sau mỗi phase: subagent `reviewer` soát nội dung, sửa xong mới làm phase test.

## Hiện trạng (đã kiểm 2026-11-14)
- `syllabus.yaml`: p6 (4 bài), p7 (10 bài, gồm 2 mini-project RAG và agent), p8 (4 bài) mới là outline: chỉ có id, title, prerequisites, chưa có outcomes. Cả ba phase đang có `runner: local`; trang Learn đã có badge "runner cục bộ".
- Chưa có runner cục bộ. Toàn bộ code đang chạy qua `apps/web/src/lib/python.ts` (`run` / `test` / `trace`) → `public/pyodide-worker.js` → `tools/pyrunner/runner.py` / `tracer.py`.
- Máy: Python 3.13, GPU RTX 4050, **không có Docker**.
- AI tutor: đã có `rag-chat` (hint 3 tầng, commit `23940af`) và tài khoản Supabase tùy chọn (`4f4f4fa`), cả hai chỉ bật khi có biến môi trường. M4 không làm thêm phần này.

## Quyết định kiến trúc (user đã chốt 2026-11-14)
1. ★ **Runner theo bài, không theo phase.** Chỉ những bài cần thư viện mà Pyodide không có mới chạy trên runner cục bộ:
   - p6 (torch, transformers);
   - p8-01 (FastAPI `TestClient` cần thread, mà Pyodide không có).
   Phần còn lại vẫn chạy trong trình duyệt:
   - p7 dùng fake LLM client viết bằng Python thuần, embedding bằng NumPy, vector store tự viết;
   - p8-02 Docker: đọc và viết Dockerfile, test kiểm nội dung file;
   - p8-03 cache và p8-04 monitoring: Python thuần.

   Cách làm: thêm trường `runner: local` ở mức bài, trong `meta.yaml`; bỏ `runner` ở mức phase. Lý do: bạn học được phase 7, phần trọng tâm của AI Engineer, mà không phải bật server, và ít thứ có thể hỏng hơn.
2. ★ **Model Hugging Face (p6-03, p6-04):** tải một lần vài model nhỏ (vd `prajjwal1/bert-tiny` khoảng 17 MB, một model sentiment nhỏ) bằng `tools/localrunner/fetch_models.py` vào cache HF. Bài học chạy với `HF_HUB_OFFLINE=1`, nên ngoài lần tải đầu không cần mạng. Phương án khác: dựng model ngẫu nhiên từ config, không cần tải, nhưng kết quả vô nghĩa nên kém về mặt sư phạm.
3. ★ **torch bản CPU**, ghim phiên bản (khoảng 200 MB, so với bản CUDA hơn 2 GB). Lý do: output tất định, máy nào cũng chạy được. GPU chỉ nhắc ở mục "Đọc thêm".
4. **Runner cục bộ** là FastAPI trong `tools/localrunner/`:
   - Lệnh chạy: `uv run python tools/localrunner/serve.py`, nghe trên `127.0.0.1:8765`.
   - Endpoint `/health`, `/run`, `/test`, `/trace`, cùng hợp đồng JSON với worker Pyodide (chạy lại `runner.py` / `tracer.py`).
   - Mỗi request chạy trong một subprocess có timeout; ảnh matplotlib trả về giống worker.
   - **Bảo mật:** chỉ bind `127.0.0.1`, chỉ nhận `Origin` của app (dev và bản build), bắt buộc một header riêng để mọi request phải qua preflight. Như vậy trang web lạ không thể gửi code tới chạy trên máy.
5. **Web:**
   - `python.ts` chọn backend theo `lesson.runner`.
   - Bài cần runner cục bộ có chip trạng thái (đã kết nối / chưa chạy). Khi runner chưa chạy thì hiện khung hướng dẫn kèm lệnh khởi động, thay cho nút Run.
   - Visualize dùng tracer của runner.
   - Mọi chuỗi giao diện qua i18n.
6. **Fake LLM cho p7:** module `pyai_llm` dùng chung (client có `chat()`, `embed()`, tool call; phản hồi theo kịch bản và tất định). Module được nạp vào Pyodide giống `runner.py` và nằm trên `sys.path` khi chạy local hay chạy pytest. Mỗi bài p7 có thêm khối `bash` không chấm, chỉ cách gọi API thật bằng key trong `.env` (không commit key).

## Quy tắc nội dung phase 6–8 (đưa vào mỗi spec, bước 1 thêm vào CONTENT_GUIDE)
- Giữ toàn bộ quy tắc "Data & ML code (phase 4+)".
- torch:
  - `torch.manual_seed(0)` ở đầu mọi khối có ngẫu nhiên;
  - in số bằng `round(x.item(), 3)` hoặc `.tolist()` sau `round`, không in tensor thô (vì repr có `tensor(...)`, dtype và device);
  - dữ liệu nhỏ, mỗi khối chạy dưới 10 giây trên CPU.
- Không gọi mạng. Model HF chỉ lấy từ cache (`local_files_only=True`). LLM chỉ dùng fake client.
- Đánh dấu bài chạy cục bộ trong `meta.yaml` (`runner: local`). Khối code của bài đó vẫn phải chạy được trong `validate.py` (CPython).
- Test exercise vẫn chỉ dùng tập con pytest mà `runner.py` hỗ trợ.

## Các bước
| Bước | Slug | Nội dung | Trạng thái |
|---|---|---|---|
| 1 | `m4-01-foundation` | Syllabus chi tiết p6–p8 (outcomes, prerequisites, `runner` theo bài); thêm torch (CPU), transformers, fastapi, httpx, uvicorn vào `pyproject.toml`; schema `runner` ở mức bài; validate/build hiểu trường mới; xác minh trong Pyodide 0.29.5 có pydantic không; quy tắc phase 6–8 vào CONTENT_GUIDE | `a94c693` |
| 2 | `m4-02-localrunner` | Server `tools/localrunner/` (`/health`, `/run`, `/test`, `/trace`, subprocess, timeout, kiểm Origin) + test | `06790e8` |
| 3 | `m4-03-runner-web` | `python.ts` chọn backend theo bài, chip trạng thái, khung hướng dẫn khi runner chưa chạy, i18n EN/VI | `b9b1215` |
| 4 | `m4-04-fetch-models` | `fetch_models.py` tải model nhỏ vào cache; validate báo lỗi rõ ràng khi thiếu cache | `27ac77d` |
| 5–8 | `m4-p6-0N-*` | p6-01 tensors & autograd, p6-02 training loop, p6-03 HF pipelines, p6-04 fine-tune nhỏ (đây là mini-project của phase 6) | p6-01 `8e210d4`; p6-02 `6e192a8`; p6-03 `8f3e5e5`; p6-04 `9f4a819` |
| 8b | `m4-p6-review-fixes` | Reviewer phase 6, sửa | `5cc30a0` |
| 9 | `m4-p6-test` | Phase test 6 | `81df246` |
| 9a | `m4-visualize-in-questions` | Ẩn Visualize khi đang làm câu hỏi; câu cần torch chạy qua runner cục bộ | `7f5b668` |
| 10 | `m4-10-fake-llm` | Module `pyai_llm` (chat, embed, tool call) + nạp vào Pyodide và local + test | `e72fa21` |
| 11–18 | `m4-p7-0N-*` | p7-01 … p7-08 (LLM API, structured output, embeddings, vector DB, RAG, tool use, agents, evals) | p7-01 `045b301`; p7-02 `139e9e6`; p7-03 `ca0ed76`; p7-04 `0dfaf4f`; p7-05 `919ad49`; p7-06 `0add225`; p7-07 `1de7ae3`; p7-08 `c133e77` |
| 19–20 | `m4-p7-09`, `m4-p7-10` | Mini-project RAG, mini-project agent (portfolio) | p7-09 `7977522`; p7-10 `7d48537` |
| 20b | `m4-p7-review-fixes-a`, `-b` | Reviewer phase 7, sửa (a: p7-01..05, b: p7-06..10; review ở `tasks/m4-p7-review.md`) | a `965d73f`; b `1bf8ade` |
| 21 | `m4-p7-test` | Phase test 7 | `f15a3a3` |
| 22–25 | `m4-p8-0N-*` | p8-01 FastAPI (local), p8-02 Docker (không chạy Docker), p8-03 caching, p8-04 monitoring, cost & latency | p8-01 `85b81fc`; p8-02 `da2612a`; p8-03 `bb6b9c4`; p8-04 `a223b3a` |
| 25a | `m4-p8-05-project` | Mini-project: đưa dịch vụ RAG lên production (FastAPI, cache, latency/cost; local) | `5fca22d` |
| 25b | `m4-p8-review-fixes` | Reviewer phase 8, sửa | đợt a `bb5a1ae`; đợt b `02e9e3d` |
| 26 | `m4-p8-test` | Phase test 8 | `e4b7dba` |
| 27 | `m4-27-docs` | Cập nhật CLAUDE.md, DESIGN.md (§5 runner, §10 M4 xong), portfolio.yaml, đọc mẫu VI khoảng 25% | docs xong (local), portfolio `3467502`; báo cáo VI ở `tasks/m4-vi-sample-review.md` |
| 27b | `m4-vi-fixes` | Sửa bản VI phase 6–8 theo đọc mẫu | `1d70a9b` |

Thứ tự: làm bước 1–3 trước để có đường chạy hoàn chỉnh, rồi tới p6. Có thể làm p7 trước p6 nếu muốn có phần trọng tâm sớm; p7 chỉ cần bước 1 và bước 10.

## Kết quả
**M4 xong 2026-11-18** (commit cuối `1d70a9b`). Việc để riêng, chưa làm:
- Nâng cấp Next.js 16.4.2 (build in cảnh báo bảo mật, lần đầu fail, chạy lại qua).
- Đưa `tasks/check_lesson_comments.py` và `tasks/check_overlap.py` vào `tools/` (validator chưa so comment output) — cần user đồng ý.
- Quiz phase 5 lộ đáp án qua độ dài phương án.

## Rủi ro
- Output torch/transformers khác nhau giữa các phiên bản → ghim phiên bản, làm tròn số, mỗi khối có seed.
- Validate chậm hơn vì phải import torch → đo thời gian ở bước 1 (hiện khoảng 165 s); nếu tăng hơn 50% thì cache kết quả theo hash bài.
- Nội dung LLM lỗi thời nhanh → `meta.yaml` mỗi bài p7 có ngày review; fake client mô phỏng dạng API chung, không chép SDK của một hãng cụ thể.
- Runner chạy code tùy ý trên máy → mục 4 (localhost, Origin, preflight).

- Follow-up xong: Next.js 16.4.5 + DOMPurify + supabase-js (`43c42e9`), cân MCQ phase 5 (`8ae8e9e`), validator comment output + cảnh báo chép code (`e099fd7`, `5c2fbe0`).
