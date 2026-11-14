# Chuẩn hóa feature bên trong Pipeline

**Ví dụ này cho thấy:** Lý do `KNeighborsClassifier` đoán kém khi một feature (`tokens`, 200–4000) lấn át hẳn feature còn lại (`error_rate`, 0.0–0.45), và cách `make_pipeline(StandardScaler(), ...)` giải quyết mà không gây rò rỉ dữ liệu.

**Từng bước**
1. Dòng 8–12 tạo 40 dòng trong đó `tokens` nhiễu ở thang đo lớn còn `error_rate` phân tách rõ lớp `0` và `1` ở thang nhỏ `[0, 0.45]`.
2. Dòng 14–16 chia dữ liệu một lần duy nhất bằng `random_state=42` và `stratify=y`.
3. Dòng 18–20 huấn luyện `KNeighborsClassifier(n_neighbors=3)` trực tiếp trên dữ liệu thô (`0.5` trên tập test — chẳng khác gì tung đồng xu).
4. Dòng 22–24 ghép `StandardScaler()` và `KNeighborsClassifier(n_neighbors=3)` trong `make_pipeline`, để bộ chuẩn hóa chỉ học thống kê từ `X_train` rồi áp dụng cho `X_test`.

**Để ý:** Khi chưa chuẩn hóa, độ lệch vài trăm token che lấp hoàn toàn độ lệch `0.1` của `error_rate` trong phép đo khoảng cách của KNN.

**Tự thử:** Đổi `n_neighbors=3` thành `1` hoặc `5` ở cả hai mô hình xem KNN không chuẩn hóa có theo kịp pipeline hay không.
