# Vòng lặp retry bằng `while` thay cho `for`

Cách làm này tự tăng biến đếm trong vòng lặp `while attempt <= max_attempts:` thay vì dùng `for attempt in range(1, max_attempts + 1):`.

Cả hai cách đều xử lý `RateLimitError` và ném lại lỗi ở lần cuối giống hệt nhau. Vòng lặp `for` với `range` thường an toàn hơn vì bạn không thể quên dòng `attempt += 1`, còn `while` lại tiện hơn khi sau này bạn muốn đổi giới hạn thử lại một cách linh hoạt ngay trong vòng lặp.
