# Mã hóa `plan` bằng boolean mask và `np.column_stack`

Thay vì tạo cột `plan_code` qua `Series.map`, cách này lọc sẵn các gói hợp lệ (`df["plan"].isin(...)`), chuyển `"pro"` và `"enterprise"` thành `0.0 / 1.0 / 2.0` trực tiếp bằng phép cộng boolean mask rồi ghép thành `X` qua `np.column_stack`. Lọc sớm tránh thêm cột phụ vào `DataFrame` và tách bạch bước kiểm tra giá trị hợp lệ, còn `Series.map` ở `solution.py` gọn hơn khi số nhóm nhiều và giữ đủ mọi cột feature trong bảng trước lúc đổi sang NumPy.
