# Ghi trace JSONL và tạo báo cáo tóm tắt cho SRE

**Những gì ví dụ minh họa:** Ghi lại các span theo từng bước `"llm"` và `"tool"` bằng `TraceRecorder`, tổng hợp chỉ số với `summarize_traces()` và xuất báo cáo terminal gọn dưới `60` ký tự mỗi dòng.

**Từng bước một**
1. Dòng 8–59 định nghĩa `FakeClock` và `TraceRecorder`, trong đó `record_step()` đo thời gian từng bước, bắt ngoại lệ thành `status="error"` và xuất JSONL đã sắp khóa qua `to_jsonl()`.
2. Dòng 62–81 cài đặt `summarize_traces()` để chỉ đếm span có `kind == "tool"` vào `tool_counts`, tính `p95_step_ms` theo nearest-rank và tính `budget_utilization`.
3. Dòng 84–93 cài đặt `format_report()` để trình bày các chỉ số SRE chính thành những dòng ngắn hơn 60 ký tự.
4. Dòng 96–107 ghi bốn bước cho `req-1` và `req-2` (gồm một lệnh `issue_refund` bị lỗi), rồi in các dòng JSONL và báo cáo tóm tắt.

**Lưu ý:** `tool_counts` chỉ chứa `lookup_order` và `issue_refund` (không tính `"fake-llm"`), `p95_step_ms` là `45.0` ms và `req-2` xuất hiện trong `failed_requests`.

**Tự thử:** Bạn hãy truyền `budget_usd=None` vào `summarize_traces()` và kiểm tra `budget_utilization` hiển thị thành `n/a` trong báo cáo.
