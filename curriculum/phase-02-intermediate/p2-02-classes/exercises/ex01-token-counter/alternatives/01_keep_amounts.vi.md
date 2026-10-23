# Giữ lại mọi số lượng

Thay vì cập nhật hai con số đang chạy, cách này lưu từng số lượng vào list `self.amounts` rồi tính `total` và `calls` từ đó bằng `sum` và `len`. Cách này dễ mở rộng về sau (ví dụ tìm số lớn nhất), nhưng tốn bộ nhớ hơn vì nhớ mọi lần gọi. `__repr__` ở đây ghép chuỗi bằng `+` và `str(...)` thay vì f-string, cho cùng kết quả.
