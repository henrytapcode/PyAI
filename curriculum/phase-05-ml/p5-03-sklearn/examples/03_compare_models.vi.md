# So sánh ba mô hình một cách công bằng

**Ví dụ này cho thấy:** Đưa `LogisticRegression`, `KNeighborsClassifier` và `DecisionTreeClassifier` qua cùng quy trình pipeline có `StandardScaler` trên một lần chia `iris` chung để có cái nhìn đầu tiên trên phần held-out.

**Từng bước**
1. Dòng 10–13 nạp bộ dữ liệu `iris` có sẵn (150 bông hoa, 3 lớp) và tạo một phép chia 70/30 có stratify với `random_state=42`.
2. Dòng 15–19 khai báo ba estimator ứng viên cùng siêu tham số rõ ràng (`max_iter=1000`, `n_neighbors=5`, `max_depth=3` với `random_state=0`).
3. Dòng 24–32 lặp qua từng ứng viên, bọc trong `make_pipeline(StandardScaler(), estimator)`, gọi `.fit(X_train, y_train)`, in ra cả điểm train lẫn held-out và ghi nhận điểm cao nhất.
4. Dòng 34 in ra ứng viên đứng đầu trên lần chia này (`DecisionTree` đạt `0.933`).

**Để ý:** Cả ba pipeline đều hòa nhau ở `0.981` trên tập train nên không thể phân biệt bằng điểm train; còn trên 45 mẫu held-out, `DecisionTree` (`0.933`, 42/45) chỉ nhỉnh hơn hai mô hình kia (`0.911`, 41/45) đúng 1 mẫu — mức chênh lệch nhỏ nằm trong may rủi của một lần chia, vì vậy ở `p5-04-evaluation` bạn sẽ dùng cross-validation trên train để chọn mô hình chắc chắn hơn.

**Tự thử:** Đổi `DecisionTreeClassifier(max_depth=3, ...)` thành `max_depth=None` — cây không giới hạn sẽ học thuộc tập train (`1.000`) và tình cờ đạt `0.978` (44/45) trên đúng tập test nhỏ này, cho thấy một lần chia đơn lẻ dao động mạnh thế nào so với cross-validation.
