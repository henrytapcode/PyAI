# Retry lũy đẳng cho LLM và ngân sách chi phí cứng

**Những gì ví dụ minh họa:** Tự động thử lại khi `FakeLLM.chat()` gặp lỗi `RateLimitError` tạm thời bằng exponential backoff (trì hoãn tăng theo cấp số nhân) trên `FakeClock`, đồng thời thực thi giới hạn `CostBudget` và gọi tool qua duck typing.

**Từng bước một**
1. Dòng 9–43 định nghĩa `FakeClock`, `Pricing` và `CostBudget` (`record(usage, pricing)` và `check()`).
2. Dòng 46–57 cài đặt `call_with_retry()` để chỉ retry `(RateLimitError, TimeoutError)` khi `idempotent=True`, tăng `clock` thêm `0.5 * 2**attempt`.
3. Dòng 60–62 định nghĩa `StubRegistry` tối giản kiểu duck typing với phương thức `.execute(name, args, ctx)`.
4. Dòng 65–85 cài đặt `run_budgeted_agent()`, kiểm tra `budget.check()` trước và sau mỗi bước gọi LLM và chỉ gọi tool đúng một lần không retry.
5. Dòng 88–95 chạy hai kịch bản: phục hồi sau `fail_times=2` lỗi tạm thời (`clock: 1.5`) và dừng ngay khi vượt `max_tokens=10`.

**Lưu ý:** Ở Run 1, hai lần retry làm `FakeClock` tiến `0.5 + 1.0 = 1.5` giây; ở Run 2, phản hồi LLM đầu tiên dùng `20` token nên `CostBudget` dừng vòng lặp với `"token_budget"` trước khi chạy bước thứ hai.

**Tự thử:** Bạn hãy giảm `max_cost_usd=0.05` ở Run 1 xuống `max_cost_usd=0.0001` và quan sát `stopped_reason` chuyển sang `"cost_budget"`.
