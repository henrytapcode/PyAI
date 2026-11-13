# So sánh ba mô hình một cách công bằng

**Ý nghĩa:** Đưa `LogisticRegression`, `KNeighborsClassifier` và `DecisionTreeClassifier` qua cùng quy trình pipeline có `StandardScaler` trên một tập chia train/test chung của bộ `iris` và chọn mô hình thắng theo điểm test.

**Từng bước**
1. Dòng 10–13 nạp bộ dữ liệu `iris` có sẵn (150 bông hoa, 3 lớp) và tạo một phép chia 70/30 có stratify với `random_state=42`.
2. Dòng 15–19 khai báo ba estimator ứng viên cùng siêu tham số rõ ràng (`max_iter=1000`, `n_neighbors=5`, `max_depth=3` với `random_state=0`).
3. Dòng 24–32 lặp qua từng ứng viên, bọc trong `make_pipeline(StandardScaler(), estimator)`, gọi `.fit(X_train, y_train)`, in ra cả điểm train lẫn test và cập nhật mô hình có điểm test cao nhất.
4. Dòng 34 in ra `DecisionTree` (`0.933`) thắng trên tập test.

**Lưu ý:** Cả ba pipeline đều hòa nhau ở `0.981` trên tập train, nên chỉ nhìn điểm train sẽ không phân biệt được — chỉ có tập test tách riêng mới phân thắng bại.

**Tự thử:** Đổi `DecisionTreeClassifier(max_depth=3, ...)` thành `max_depth=None` rồi xem cây sâu hơn có thắng thêm hay bị overfit trên tập test.
