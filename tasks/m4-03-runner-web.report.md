# Báo cáo M4 bước 3: nối runner cục bộ vào web app

## 1. Đã làm gì
- Tạo client `LocalRunner` (`apps/web/src/lib/local-runner.ts`) giao tiếp với `tools/localrunner/serve.py` qua `NEXT_PUBLIC_LOCAL_RUNNER_URL` (mặc định `http://127.0.0.1:8765`):
  - Trạng thái `"unknown" | "checking" | "connected" | "offline" | "running"`, `subscribe()`, hook `useLocalRunnerStatus()` dùng `useSyncExternalStore`, lưu `info` (`python`, `torch`, `transformers`) từ `GET /health`.
  - `check()` dùng `AbortController` timeout 3 s, kiểm tra `protocol === 1`, giữ nguyên trạng thái `running` nếu đang có job chạy.
  - `run()`, `test()`, `trace()` gửi `POST` kèm header `X-PyAI-Runner: 1`, tuần tự hóa qua hàng đợi `enqueue()`, áp dụng client timeout (130 s / 70 s / 40 s), `stop()` abort request hiện tại và trả `stopped: true`, lỗi kết nối đặt `offline` và trả `offline: true` (dùng type mở rộng `LocalTestRunResult` / `LocalTraceResult` để không sửa `types.ts`).
  - Xuất `RunnerContext` và `useRunner()` để truyền `runner` của bài học xuống `CodeBlock` trong Markdown.
- **Cách xử lý NDJSON tách chunk trong `LocalRunner.run()`**:
  - Đọc stream `response.body.getReader()` bằng `TextDecoder("utf-8")` với `{ stream: true }`.
  - Tích lũy vào `buffer`, tách theo ký tự xuống dòng `"\n"` trong vòng lặp `while ((nl = buffer.indexOf("\n")) !== -1)` để giữ phần dòng dở dang sang chunk tiếp theo.
  - Sau khi stream kết thúc (`done`), gọi `decoder.decode()` để flush phần byte còn lại và xử lý nốt `buffer` nếu không rỗng.
  - Mỗi dòng không rỗng được `JSON.parse`: `stdout`/`stderr` đẩy vào `onOutput(text, stream)`, `image` đẩy vào `onOutput(data, "image")`, `done` chốt `{ ok, error, timedOut }`.
- Cập nhật `apps/web/src/lib/python.ts`: thêm `RunnerKind`, `offline?: boolean` trên `RunResult`, và `runnerFor(runner?: RunnerKind)` trả về `{ run, test, trace, stop }` bọc `python` hoặc `localRunner`, giữ nguyên hành vi Pyodide cho các call site không truyền `runner`.
- Tạo component `LocalRunnerSetup` (`apps/web/src/components/local-runner-setup.tsx`):
  - Hướng dẫn ngắn gọn, khối lệnh `uv run python tools/localrunner/serve.py` kèm nút sao chép.
  - Khi `window.location.origin` khác `http://localhost:3000` và `http://127.0.0.1:3000`, hiển thị thêm gợi ý và lệnh kèm `--allow-origin <origin>`.
  - Nút "Thử kết nối lại" gọi `localRunner.check()`, hiện spinner khi đang kiểm, gọi `onConnected` khi kết nối thành công.
- Cập nhật `apps/web/src/components/workbench.tsx`:
  - Thêm prop `runner?: RunnerKind`; khi `runner === "local"` thì gọi `localRunner.check()` khi mount (không `python.warmUp()`), hiển thị `LocalRunnerStatus` với chấm màu và tooltip phiên bản Python/torch hoặc trạng thái offline.
  - Khi bấm Run/Check nếu chưa `connected` thì `check()` trước; nếu offline hoặc mất kết nối giữa chừng (`res.offline`) thì hiển thị `LocalRunnerSetup` trong panel output.
  - Stop gọi `runnerFor(runner).stop()`; giữ nguyên xử lý `timedOut`, `stopped`, tô dòng lỗi và UI kết quả.
- Cập nhật `apps/web/src/components/visualizer.tsx` và `apps/web/src/components/markdown.tsx`:
  - `visualize(code, runner?)` truyền `runner` vào `VisualizerHost` và `Visualizer`, gọi `runnerFor(runner).trace(code)`.
  - Nếu trace trả `offline: true`, hiển thị `LocalRunnerSetup` trong dialog và tự trace lại sau khi kết nối lại thành công.
  - `markdown.tsx` đọc `useRunner()` từ context để truyền vào `visualize(code, runner)`.
- Cập nhật `apps/web/src/components/lesson/lesson-view.tsx`: bọc với `RunnerContext.Provider value={meta.runner}` và truyền `runner={meta.runner}` vào cả 2 `Workbench` (exercise và scratch).
- Cập nhật `apps/web/src/app/(main)/playground/page.tsx`: thêm công tắc "Trình duyệt (Pyodide)" / "Runner cục bộ" lưu `localStorage` key `pyai-playground-runner` trong `try/catch`, truyền `runner` vào `Workbench`, và thêm template `torch` tự chuyển sang runner cục bộ khi chọn.
- Thêm chuỗi i18n đầy đủ cho EN/VI trong `apps/web/messages/en.json` và `apps/web/messages/vi.json` (`editor.runner*` và nhóm `localRunner`).

## 2. File đã sửa / tạo
- Tạo mới:
  - `apps/web/src/lib/local-runner.ts`
  - `apps/web/src/components/local-runner-setup.tsx`
  - `tasks/m4-03-runner-web.report.md`
- Đã sửa:
  - `apps/web/src/lib/python.ts`
  - `apps/web/src/components/workbench.tsx`
  - `apps/web/src/components/visualizer.tsx`
  - `apps/web/src/components/markdown.tsx`
  - `apps/web/src/components/lesson/lesson-view.tsx`
  - `apps/web/src/app/(main)/playground/page.tsx`
  - `apps/web/messages/en.json`
  - `apps/web/messages/vi.json`

## 3. Kết quả lệnh kiểm tra
- `pnpm.cmd --filter web typecheck` (chạy `pnpm run content && tsc --noEmit`; lưu ý `pnpm` trên PowerShell bị chặn ExecutionPolicy cho `pnpm.ps1` nên dùng `pnpm.cmd`): **PASS** (exit code 0, built 35 lessons, 8 exams, 210 flashcards, 563 questions, `tsc --noEmit` không lỗi).
- `uv run python -m pytest tools/localrunner -q`: **PASS** (16 passed).
- Smoke test `tools/localrunner/serve.py` trên port tạm `18765` bằng script Node tạm (đã dừng server và xóa script tạm):
  - `GET /health`: trả `{"ok":true,"protocol":1,"python":"3.13.15","torch":"2.15.0+cpu","transformers":"5.23.0"}`.
  - `POST /run` với header `X-PyAI-Runner: 1`: stream NDJSON tách dòng hợp lệ (`stdout` rồi `done`).
  - `POST /test`, `POST /trace`: trả JSON hợp lệ (`trace steps: 3, error: null`).
- `git status --short`: chỉ gồm các file được phép trong spec (ngoài `tasks/`, `.hallmark/`).

## 4. Điều còn chưa chắc / chưa tự kiểm được
- Theo ràng buộc task, không chạy `pnpm --filter web build` và không chạy Next.js dev server nên chưa kiểm tra trực tiếp trên trình duyệt:
  - CORS / Private Network Access preflight giữa trình duyệt (`http://localhost:3000`) và `127.0.0.1:8765`.
  - Giao diện thực tế của `LocalRunnerSetup`, `LocalRunnerStatus`, `Playground`, `Visualizer` ở cả desktop và mobile 375px (light/dark mode, copy clipboard, tooltip, spinner, auto-retry sau khi bấm "Thử kết nối lại").
  - Tình huống mất kết nối giữa chừng khi đang stream `/run` hoặc đang chạy `/test` trên UI thật, cũng như hành vi timeout/stop qua UI.

## Vòng 2
### 1. Đã sửa theo feedback vòng 1
- **Gom dòng theo từng stream trong `apps/web/src/lib/local-runner.ts`**:
  - Thêm hằng số `OUTPUT_FLUSH_MS = 150` và bộ đệm `createStreamBuffer(onOutput)` giữ buffer riêng cho `stdout` và `stderr` cùng danh sách `pendingOrder` để giữ thứ tự nhận giữa hai stream khi flush.
  - Khi nhận chunk `stdout`/`stderr`, tích lũy vào buffer của stream tương ứng và tách theo `"\n"`, gọi `onOutput(line + "\n", stream)` cho từng dòng hoàn chỉnh để mỗi `print(...)` gom thành một dòng giống Pyodide (không sửa `workbench.tsx` hay server).
  - Phần chưa có `"\n"` được tự flush sau `OUTPUT_FLUSH_MS` (150 ms) không nhận thêm dữ liệu trên stream đó, và flush toàn bộ phần dở dang khi gặp `image`, `done`, khi stream kết thúc, khi lỗi, Stop hoặc timeout (`dispose()` dọn timer trong `finally`).
- **Sửa layout header Playground trong `apps/web/src/app/(main)/playground/page.tsx`**:
  - Đổi thanh header sang `lg:flex-row lg:items-center lg:justify-between` (thay cho `sm:flex-row sm:items-center sm:justify-between`), thêm `lg:min-w-56` cho khối tiêu đề và `lg:justify-end` cho cụm nút bên phải.
  - Kiểm tra class theo breakpoint: ở 375 px và 800 px (`< lg`), header xếp dọc nên khối tiêu đề chiếm toàn bộ chiều rộng; ở 1280 px (`>= lg`), khối tiêu đề giữ tối thiểu `min-w-56` (14rem / 224px), không bị bóp hẹp hơn "Sân chơi code".

### 2. Kiểm tra lại sau sửa vòng 2
- `pnpm.cmd --filter web typecheck`: **PASS** (exit code 0, built 35 lessons, 8 exams, 210 flashcards, 563 questions, `tsc --noEmit` không lỗi).
- `uv run python -m pytest tools/localrunner -q`: **PASS** (`16 passed`).
- Kiểm tra unit logic `LocalRunner.run()` (6 test cases trong script tạm ở thư mục scratch của conversation, mock `fetch` stream): kiểm tra gom mảnh `print("loss:", 3.439)` + xen kẽ `stderr`, flush sau `150 ms` với `print(..., end="")`, giữ thứ tự `stderr`/`stdout` khi flush ở `done`, flush khi stream kết thúc không có `done`, khi lỗi giữa chừng và khi `stop()` — **6/6 PASS**.
- `git status --short`: chỉ gồm các file trong danh sách cho phép (và `tasks/`, `.hallmark/`).
