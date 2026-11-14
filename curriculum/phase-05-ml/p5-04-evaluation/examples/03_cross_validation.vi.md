# Cross-validation phân tầng để so sánh ba mô hình

**Ví dụ này cho thấy:** So sánh ba bộ phân loại (`LogisticRegression`, `KNeighborsClassifier` và `DecisionTreeClassifier`) trên bộ dữ liệu `load_breast_cancer` (đã đảo nhãn để `1` = ác tính) bằng `StratifiedKFold` 5 fold và điểm `f1` bên trong `make_pipeline`.

**Từng bước**
1. Dòng 12–15 nạp bộ dữ liệu `load_breast_cancer` có sẵn (569 hàng) và đảo `y = 1 - y` để lớp `1` là u ác tính (212 ác tính, 357 lành tính).
2. Dòng 17–22 khởi tạo `StratifiedKFold` 5 fold tái lập được và danh sách ba mô hình ứng viên.
3. Dòng 27–35 bọc từng ứng viên trong `make_pipeline(StandardScaler(), estimator)`, chạy `cross_val_score(..., scoring="f1")` qua 5 fold rồi in `mean` và `std` làm tròn 3 chữ số.
4. Dòng 37 in mô hình tốt nhất (`LogReg` với F1 `0.971`).

**Để ý:** Đảo nhãn `y = 1 - y` giúp F1 đo đúng khả năng phát hiện u ác tính thay vì u lành, còn đặt `StandardScaler()` bên trong `make_pipeline` bảo đảm mỗi fold chỉ fit bộ chuẩn hóa trên đúng 4 fold train của nó.

**Tự thử:** Đổi `scoring="f1"` ở dòng 29 thành `scoring="recall"` — vì lớp `1` là u ác tính, recall lúc này đo tỉ lệ ca ung thư thật mà mỗi mô hình bắt được (`LogReg` đạt `0.958`).
