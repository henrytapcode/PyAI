# Bộ phân loại độ khẩn cấp của ticket

**Ý nghĩa:** Chia 24 ticket hỗ trợ đã gắn nhãn bằng `train_test_split(..., stratify=y)`, huấn luyện bộ phân loại `LogisticRegression`, đo accuracy trên tập test và dự đoán cho ba ticket mới.

**Từng bước**
1. Dòng 6–10 tạo 24 ticket mô phỏng với hai feature số (`tokens` và `links`) cùng nhãn cân bằng (`0` bình thường, `1` khẩn cấp).
2. Dòng 12–14 tách 25% số hàng sang tập test với `random_state=42` và `stratify=y` để cả train lẫn test giữ nguyên tỉ lệ 50/50.
3. Dòng 16–19 khởi tạo `LogisticRegression(max_iter=1000)`, gọi `.fit(X_train, y_train)` và in ra test accuracy đã làm tròn (`0.833`).
4. Dòng 21–23 gọi `.predict(new_tickets).tolist()` để phân loại ba ticket mới thành list số nguyên Python thuần.

**Lưu ý:** Vì khoảng token của nhóm bình thường (`20..159`) và khẩn cấp (`120..319`) có giao nhẹ, test accuracy đạt `0.833` (đúng 5 trên 6 ticket test) thay vì `1.0` đáng ngờ.

**Tự thử:** Đổi `test_size=0.25` thành `0.3` hoặc tăng số `links` của ticket thứ ba (`[95.0, 1.0]`) lên `[95.0, 5.0]` rồi xem kết quả dự đoán thay đổi thế nào.
