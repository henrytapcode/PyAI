# Cross-validation phân tầng để so sánh ba mô hình

**Ví dụ này minh họa:** So sánh ba bộ phân loại (`LogisticRegression`, `KNeighborsClassifier` và `DecisionTreeClassifier`) trên bộ dữ liệu `load_breast_cancer` bằng `StratifiedKFold` 5 fold và điểm `f1` bên trong `make_pipeline`.

**Từng bước**
1. Dòng 12–13 nạp bộ dữ liệu `load_breast_cancer` có sẵn (569 hàng, phân bố lớp `[212, 357]`).
2. Dòng 15–20 khởi tạo `StratifiedKFold` 5 fold tái lập được và danh sách ba mô hình ứng viên.
3. Dòng 25–33 bọc từng ứng viên trong `make_pipeline(StandardScaler(), estimator)`, chạy `cross_val_score(..., scoring="f1")` qua 5 fold rồi in `mean` và `std` làm tròn 3 chữ số.
4. Dòng 35 in mô hình tốt nhất (`LogReg` với F1 `0.983`).

**Điểm đáng chú ý:** Đặt `StandardScaler()` bên trong `make_pipeline` bảo đảm mỗi fold trong 5 fold chỉ fit bước chuẩn hóa trên đúng 4 fold train của nó, tránh rò rỉ dữ liệu giữa các fold.

**Tự thử thêm:** Đổi `scoring="f1"` ở dòng 27 thành `scoring="recall"` xem thứ hạng hay độ lệch chuẩn có đổi không.
