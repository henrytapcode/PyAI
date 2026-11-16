# Ghi log request có cấu trúc với FakeLLM

**Ví dụ này minh họa gì:** Ghi 8 request LLM giả lập thành từng dòng JSON qua `logging` ra `sys.stdout`, bao gồm trúng cache, trượt cache và một lỗi `RateLimitError`.

**Từng bước**
1. Dòng 13–18 định nghĩa `FakeClock` để độ trễ tăng tất định (`2.0` ms khi trúng cache, `200 + 3 * completion_tokens` ms khi gọi model, và `150.0` ms khi lỗi).
2. Dòng 22–28 cấu hình logger `"app.metrics"` với `stream=sys.stdout` và `format="%(message)s"` để mỗi dòng xuất ra là một JSON nguyên vẹn.
3. Dòng 46–82 chạy 8 request: `req-01` gặp `RateLimitError` (`fail_times=1`) và ghi `status="error"` với 0 token, `req-05` và `req-07` trúng cache với `0` token, 5 request còn lại gọi `FakeLLM` và tính `cost_usd`.
4. Dòng 84 in `logged_lines: 8`, cho thấy request lỗi vẫn được ghi nhận đầy đủ như request thành công.

**Điểm cần chú ý:** `req-01` bị lỗi trước khi model trả kết quả, nhưng bản ghi có cấu trúc của nó vẫn được log với `status="error"` và `latency_ms=150.0` để phép tính error rate không bị sai lệch.

**Tự thử thêm:** Đổi `FakeLLM(fail_times=1)` thành `FakeLLM(fail_times=2)` và quan sát cả `req-01` lẫn `req-02` đều ghi `"status": "error"` thay vì biến mất âm thầm.
