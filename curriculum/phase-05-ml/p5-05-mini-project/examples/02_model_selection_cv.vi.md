# Chọn mô hình bằng cross-validation 5 fold có phân tầng

**Ví dụ này cho thấy:** Làm sạch log ticket thô, tách riêng 25% làm tập test rồi so sánh baseline `DummyClassifier`, pipeline `LogisticRegression` và `DecisionTreeClassifier` trên tập train bằng F1 qua 5 fold phân tầng.

**Từng bước**
1. Các dòng 34–41 chuẩn hóa `plan` và `tokens`, bỏ dòng trùng `ticket_id` (`keep="first"`), mã hóa `plan` thành `0.0/1.0/2.0` và bỏ dòng thiếu số liệu đồng thời loại bỏ cột `escalated_to_oncall`.
2. Các dòng 43–46 tạo `X` và `y` (`231` dòng sạch) rồi chia `75/25` có `stratify=y` (`173` train, `58` test).
3. Các dòng 48–54 cấu hình `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` và `make_scorer(f1_score, zero_division=0)` để ghi rõ cách xử lý khi một fold có mẫu số bằng 0.
4. Các dòng 56–66 chạy `cross_val_score` chỉ trên `(X_train, y_train)`, in `mean` và `std` F1 của từng mô hình và chọn `logreg` (`0.709 +/- 0.092` so với `0.701 +/- 0.140`).

**Để ý:** Cả `logreg` (`0.709`) và `tree` (`0.701`) đều vượt xa `baseline` (`0.000`), nhưng mức chênh giữa hai mô hình (`0.008`) nhỏ hơn hẳn độ lệch chuẩn giữa các fold (`0.092` và `0.140`).

**Tự thử:** Đổi `DecisionTreeClassifier(max_depth=3, random_state=0)` thành `max_depth=5` xem CV F1 tăng lên hay `std` nở rộng hơn.
