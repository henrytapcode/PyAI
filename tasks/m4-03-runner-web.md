# M4 bước 3: nối runner cục bộ vào web app

## Mục tiêu
Bài có `runner: local` chạy Run, Check và Visualize qua server `tools/localrunner/` (commit `06790e8`) thay cho Pyodide.
- Khi runner chưa bật, người học thấy hướng dẫn bật rõ ràng, không bị lỗi khó hiểu.
- Bài khác vẫn chạy Pyodide **y như cũ**.
- Playground có thêm công tắc chọn nơi chạy, để thử torch tự do và để boss kiểm bước này khi chưa có bài p6 nào.

Hợp đồng server: đọc `tools/localrunner/README.md` và `tools/localrunner/server.py`.
- `POST /run` trả về NDJSON gồm các message `stdout`, `stderr`, `image`, rồi một message `done`.
- `/test` và `/trace` trả về JSON giống hệt worker Pyodide.
- Mọi `POST` gửi kèm header `X-PyAI-Runner: 1`.

## File được phép sửa/tạo
- `apps/web/src/lib/local-runner.ts` (mới)
- `apps/web/src/lib/python.ts`
- `apps/web/src/components/workbench.tsx`
- `apps/web/src/components/local-runner-setup.tsx` (mới)
- `apps/web/src/components/visualizer.tsx`
- `apps/web/src/components/markdown.tsx`: chỉ chỗ gọi `visualize`
- `apps/web/src/components/lesson/lesson-view.tsx`: chỉ truyền `runner`
- `apps/web/src/app/(main)/playground/page.tsx`
- `apps/web/messages/en.json`, `apps/web/messages/vi.json`
- `tasks/m4-03-runner-web.report.md`

## Không được đụng
- `tools/`, `curriculum/`, `apps/web/public/`, `src/generated/`, mọi file khác. Không xóa file, không `git commit`.
- **Không chạy `pnpm --filter web build` và không chạy dev server.** Boss sẽ chạy cả hai.

## Thiết kế (boss chốt)

### `lib/local-runner.ts`
- URL gốc: `process.env.NEXT_PUBLIC_LOCAL_RUNNER_URL || "http://127.0.0.1:8765"`.
- `class LocalRunner`, xuất một instance `localRunner` (chỉ tạo khi có `window`, giống `python`).
- Trạng thái: `"unknown" | "checking" | "connected" | "offline" | "running"`.
  - Có `subscribe` và hook `useLocalRunnerStatus()` dùng `useSyncExternalStore`, giống `usePythonStatus`.
  - Lưu `info` từ `/health` (`python`, `torch`).
- `check(): Promise<boolean>`:
  - `GET /health`, timeout 3 s bằng `AbortController`;
  - thành công và `protocol === 1` thì `connected`, mọi lỗi thì `offline`;
  - nếu đang `running` thì giữ nguyên trạng thái.
- `run(code, onOutput): Promise<RunResult>`:
  - `fetch` POST `/run`, đọc `response.body` bằng reader, tách theo dòng (giữ phần dở dang giữa các chunk), `JSON.parse` từng dòng;
  - `stdout`/`stderr` gọi `onOutput(text, stream)`; `image` gọi `onOutput(data, "image")`;
  - gặp `done` thì trả `{ok, error, timedOut?}`.
- `test(code, tests)` và `trace(code)`: POST, trả về JSON.
- Timeout phía client, để phòng server treo: run 130 s, test 70 s, trace 40 s. Quá giờ thì abort và trả kết quả `timedOut: true`, đúng dạng mà `python.ts` đang trả khi quá giờ.
- Request không gửi được (server tắt giữa chừng): đặt `offline`, trả `{ok:false, error:null, offline:true}`. Với test/trace thì trả dạng rỗng tương ứng cộng `offline: true`. Thêm `offline?: boolean` vào `RunResult` (`python.ts`) và vào `TestRunResult` / `TraceResult` nếu cần; định nghĩa `offline` ngay trong `local-runner.ts` hoặc mở rộng type tại chỗ dùng. **Không sửa `types.ts`**: nếu cần thì dùng intersection type.
- `stop()`: abort request đang chạy (server sẽ kill process con), resolve với `stopped: true`.
- Mỗi lúc chỉ một request. Request mới khi đang chạy thì đợi request trước xong.

### Chọn backend (`python.ts`)
- Thêm `export type RunnerKind = "pyodide" | "local"` và `export function runnerFor(runner?: "local")`.
- Hàm này trả một object có `run`, `test`, `trace`, `stop` cùng chữ ký với `PythonManager`.
  - `stop` ứng với `restart({stopped:true})` của Pyodide.
  - Pyodide: bọc `python`. Local: bọc `localRunner`.
- **Không đổi hành vi Pyodide**: các call site cũ không truyền `runner` thì vẫn y như trước.

### Workbench
- Prop mới `runner?: "local"`.
- Khi `runner === "local"`:
  - **không** gọi `python.warmUp()`; khi mount thì gọi `localRunner.check()`;
  - chỗ `PythonStatus` thay bằng `LocalRunnerStatus`: chấm màu (connected: `bg-primary`; checking/running: nhấp nháy; offline: `bg-danger`) và chữ "Local runner". Tooltip ghi phiên bản Python/torch khi đã kết nối, hoặc "chưa kết nối";
  - bấm Run/Check: nếu trạng thái chưa phải `connected` thì `check()` trước. Vẫn offline thì **không chạy**, mà hiện `LocalRunnerSetup` trong panel output;
  - nút Stop gọi `stop()` của backend local;
  - kết quả `offline: true` giữa chừng cũng hiện `LocalRunnerSetup`.
- Run/Check/Stop/kết quả hiển thị giống hệt Pyodide: cùng panel, cùng xử lý `timedOut`, `stopped`, cùng tô dòng lỗi.

### `LocalRunnerSetup` (component mới)
Khung hướng dẫn gọn, dùng token màu có sẵn (`apps/web/design.md`), đọc tốt ở 375px:
- Tiêu đề và một câu: bài này cần runner cục bộ vì dùng thư viện (torch, transformers, FastAPI) không chạy được trong trình duyệt.
- Lệnh trong khối mono có nút copy: `uv run python tools/localrunner/serve.py` (kèm câu "chạy ở thư mục gốc của repo").
- Nếu `window.location.origin` không phải `http://localhost:3000` hay `http://127.0.0.1:3000`: thêm một dòng nói cần cho phép origin này, kèm lệnh đầy đủ có `--allow-origin <origin hiện tại>`.
- Nút "Thử kết nối lại" gọi `check()`; khi đang kiểm thì hiện spinner.
- Mọi chuỗi qua i18n, nhóm `localRunner`, có cả EN và VI. VI tự nhiên, thuật ngữ giữ tiếng Anh.

### Visualize
- `visualize(code, runner?: "local")`. `VisualizerHost` lưu `runner` vào state; `Visualizer` gọi `runnerFor(runner).trace(code)`.
- Kết quả có `offline` thì hiện `LocalRunnerSetup` trong dialog (bấm "Thử kết nối lại" xong thì chạy lại trace).
- Mã nguồn bài học: `lesson-view.tsx` cung cấp `runner` của bài (`lesson.meta.runner`) qua một React context nhỏ (export từ `local-runner.ts` hoặc `markdown.tsx`), `markdown.tsx` đọc context đó để gọi `visualize(code, runner)`. Hai `Workbench` trong `lesson-view.tsx` nhận `runner={lesson.meta.runner}`.

### Playground
- Thêm công tắc hai lựa chọn "Trình duyệt (Pyodide)" / "Runner cục bộ", đặt cạnh các nút template, cùng kiểu nút.
- Lưu lựa chọn vào `localStorage` key `pyai-playground-runner`, đọc/ghi trong `try/catch`.
- Truyền `runner` vào `Workbench`.
- Thêm template `torch`:
  ```python
  import torch

  torch.manual_seed(0)
  x = torch.randn(3, 2)
  w = torch.ones(2, requires_grad=True)
  loss = (x @ w).pow(2).mean()
  loss.backward()
  print("loss:", round(loss.item(), 3))
  print("grad:", [round(g, 3) for g in w.grad.tolist()])
  ```
  Chọn template `torch` thì tự chuyển sang Runner cục bộ.

## Tiêu chí hoàn thành (checklist)
1. [ ] Bài không có `runner` và playground ở chế độ Pyodide chạy y như cũ; `git diff` của các call site Pyodide chỉ thêm prop, không đổi logic.
2. [ ] Runner local: Run stream output, Check ra kết quả test, Visualize chạy qua `/trace`, Stop dừng được, timeout hiển thị đúng.
3. [ ] Runner tắt: thấy `LocalRunnerSetup` (không có lỗi đỏ khó hiểu); bật runner, bấm "Thử kết nối lại" là chạy được.
4. [ ] i18n đủ EN/VI, không chuỗi cứng; typecheck xanh.
5. [ ] Report: liệt kê file đã đổi, cách xử lý NDJSON tách chunk, những gì chưa tự kiểm được (vì không chạy dev server).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
pnpm --filter web typecheck
uv run python -m pytest tools/localrunner -q
git status --short
```
Mong đợi: tất cả xanh; `git status` chỉ có file được phép (ngoài `tasks/`, `.hallmark/`).
(Web chưa có script `lint`; typecheck là cổng chính.)

## Ghi chú cho worker
- Có thể bật `uv run python tools/localrunner/serve.py` để thử `fetch` bằng script Node nhỏ trong thư mục tạm (không để lại file trong repo). Dừng server trước khi kết thúc.
- Đọc `apps/web/design.md` trước khi làm UI.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm trên app: offline → khung hướng dẫn, kết nối lại, Run torch liền dòng, Stop kill child, /trace qua CORS, Pyodide + Visualize bài cũ vẫn chạy, header 375/900/1280 ổn; typecheck + build + 16 test xanh; đã commit `b9b1215`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Ghi chú vòng 1 (lần gọi lại)
Lần trước worker bị kẹt 30 phút vì chạy `serve.py` ở foreground (lệnh không bao giờ trả về), boss đã tắt server. Code đã sửa gần hết nhưng chưa có report và chưa chạy lệnh kiểm tra.
- **Không chạy `serve.py` ở foreground.** Nếu cần thử thì chạy nền bằng PowerShell `Start-Process -PassThru` (ghi lại PID), thử xong `Stop-Process -Id <PID>`. Mọi lệnh khác phải tự kết thúc.

## Feedback vòng 1
Boss đã kiểm trên app (dev server + runner thật): khung hướng dẫn khi runner tắt, "Thử kết nối lại", Run torch, Stop (process con bị kill), `/trace` qua CORS, và Pyodide vẫn chạy như cũ. Còn 2 lỗi:

1. **Output bị vỡ dòng ở runner cục bộ.** Server gửi stdout theo từng mẩu (`print("loss:", 3.439)` đến thành `"loss:"`, `" "`, `"3.439"`, `"\n"`), còn Workbench vẽ mỗi lần `onOutput` thành một khối riêng. Kết quả là `loss:` và ` 3.439` nằm trên hai dòng; vòng lặp `print('tick', i)` ra `tick` / ` ` / `2` lộn xộn. Pyodide gửi mỗi lần một dòng hoàn chỉnh (`text + "\n"`).
   - Sửa trong `lib/local-runner.ts`: giữ một buffer riêng cho từng stream (`stdout`, `stderr`). Mỗi khi có `"\n"` thì gọi `onOutput(line + "\n", stream)` cho từng dòng hoàn chỉnh.
   - Phần dở dang thì flush khi gặp `done`, khi stream kết thúc, khi lỗi, Stop hay timeout, và khi stream đó không nhận thêm gì trong 150 ms (cho trường hợp `print(..., end="")` hoặc thanh tiến trình). Thêm hằng số `OUTPUT_FLUSH_MS = 150`.
   - Thứ tự giữa stdout và stderr giữ theo thứ tự nhận.
   - **Không** sửa `workbench.tsx` hay server cho việc này.
2. **Tiêu đề playground bị bóp thành cột chữ dọc** ở bề rộng khoảng 800–1100 px: cụm "Nơi chạy" + "Mẫu" ở bên phải quá rộng nên `div` tiêu đề (`min-w-0 flex-1`) co về gần 0.
   - Sửa trong `playground/page.tsx`: header chỉ chuyển sang hàng ngang từ `lg:` (`lg:flex-row lg:items-center lg:justify-between`, thay cho `sm:`), và cho tiêu đề `lg:min-w-56`. Cụm nút bên phải `lg:justify-end`.
   - Tự kiểm bằng cách đọc class: ở 375, 800 và 1280 px tiêu đề không bao giờ hẹp hơn chữ "Sân chơi code".

Chạy lại lệnh kiểm tra và cập nhật report (thêm mục "Vòng 2"). Nhớ quy tắc: không chạy `serve.py` hay dev server ở foreground.
