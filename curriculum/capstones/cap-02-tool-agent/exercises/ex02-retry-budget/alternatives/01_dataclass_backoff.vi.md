# Dataclass bất biến cho bảng giá và vòng lặp `while` nhân đôi delay

Cách tiếp cận này mô hình hóa `Pricing` bằng `@dataclass(frozen=True)` bất biến và `CostBudget` bằng `@dataclass` có kiểm tra hợp lệ trong `__post_init__`, giúp tránh sửa nhầm đơn giá sau khi khởi tạo. Trong `call_with_retry`, hàm nhân đôi `delay *= 2.0` tuần tự bên trong vòng lặp `while True` thay vì tính lại `base_delay * (2 ** attempt)` ở mỗi lần thử. Cả hai cách đều có độ phức tạp thời gian `O(max_retries)` và bộ nhớ `O(1)`, trong đó dataclass bất biến an toàn hơn khi chia sẻ cấu hình giá qua nhiều lượt chạy agent.
