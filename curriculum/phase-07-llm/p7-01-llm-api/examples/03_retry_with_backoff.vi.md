# Retry lỗi tạm thời với exponential backoff

**Điều cần thấy:** Bọc `client.chat(...)` trong vòng lặp `for` để bắt `RateLimitError`, in thời gian chờ tăng gấp đôi mỗi lượt (`0.5s`, `1.0s`, `2.0s`), và ném lại lỗi nếu hết lượt thử.

**Từng bước**
1. Dòng 5–20 định nghĩa `call_with_retry(client, messages, max_attempts=3)` dùng vòng lặp `for` từ `1` tới `max_attempts`.
2. Dòng 11–14 gọi `client.chat(messages)` trong khối `try` và trả về ngay `resp.content` nếu thành công.
3. Dòng 15–19 bắt `RateLimitError`, tính thời gian chờ lũy tiến `0.5 * 2 ** (attempt - 1)`, chỉ in ra thay vì ngủ thật, và dùng `raise` ở lần thử cuối cùng.
4. Dòng 23–33 minh họa cả hai tình huống: `FakeLLM(fail_times=2)` thành công ở lần 3, còn `FakeLLM(fail_times=5)` dùng hết 3 lượt và để `RateLimitError` văng ra khối `except` bên ngoài.

**Lưu ý:** Dòng `if attempt == max_attempts: raise` đảm bảo chương trình không nuốt mất lỗi khi mọi lượt thử đều thất bại.

**Thử tự sửa:** Đổi `max_attempts=3` thành `max_attempts=6` ở Case 2 và xem `FakeLLM(fail_times=5)` thành công ở lần thử thứ 6.
