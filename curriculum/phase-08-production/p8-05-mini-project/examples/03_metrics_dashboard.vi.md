# Bảng chỉ số metric và cảnh báo

**Ví dụ này cho thấy:** Cách `/ask` ghi nhận độ trễ mô phỏng tất định (`0.2 + 0.002 * completion_tokens`), chi phí token và cache hit, cùng cách `GET /metrics` tổng hợp `p50_ms`, `p95_ms`, `total_cost` và cảnh báo ngưỡng.

**Từng bước**
1. Các dòng 31–43 định nghĩa `SlowClient`, gọi `clock.advance(...)` trong `chat()` theo công thức cố định nên request trượt cache mất hơn 200 ms còn cache hit ở mức `0.0` ms.
2. Các dòng 57–133 đo `t0 = clock()` và `clock() - t0` trong `/ask`, lưu một bản ghi metric cho mỗi request hợp lệ.
3. Các dòng 136–164 mô phỏng 12 request (gồm một payload lỗi `422` bị Pydantic chặn trước khi vào `/ask`) rồi in bảng `/metrics` và danh sách cảnh báo.

**Để ý:** `requests` là `11` thay vì `12` vì Pydantic chặn payload rỗng ngay ở cửa vào (`422`) trước khi hàm xử lý `/ask` kịp chạy.

**Tự thử:** Tăng `max_p95_ms` lên `250.0` và `max_cost` lên `0.0005` trong `create_app` rồi kiểm tra `alerts` trở về `[]`.
