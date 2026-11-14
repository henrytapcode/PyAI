# Đánh giá mô hình phân loại ticket lệch lớp

**Ví dụ này cho thấy:** So sánh baseline `DummyClassifier` với pipeline `LogisticRegression` trên bộ dữ liệu lệch lớp 85/15 bằng accuracy, confusion matrix, precision, recall, F1 và `classification_report`.

**Từng bước**
1. Dòng 18–23 tạo 200 ticket giả lập với tỉ lệ lớp 85/15 và chia train/test 70/30 giữ nguyên tỉ lệ lớp (`51` bình thường, `9` khẩn cấp ở tập test).
2. Dòng 25–29 huấn luyện cả `DummyClassifier(strategy="most_frequent")` lẫn pipeline `StandardScaler` + `LogisticRegression`, rồi dự đoán trên `X_test`.
3. Dòng 31–37 đối chiếu accuracy (`0.85`) và recall (`0.0`, truyền `zero_division=0`) của baseline với accuracy của mô hình (`0.883`).
4. Dòng 38–45 in confusion matrix `[[51, 0], [7, 2]]`, bộ ba precision/recall/F1 (`1.0`, `0.222`, `0.364`) và bảng `classification_report` đầy đủ.

**Để ý:** Accuracy tăng từ `0.85` lên `0.883`, nhưng confusion matrix cho thấy mô hình bỏ sót tới `7` trong `9` ticket khẩn cấp (`recall = 0.222`).

**Tự thử:** Đổi `LogisticRegression()` sang `DecisionTreeClassifier(max_depth=3, random_state=0)` (import từ `sklearn.tree`) xem precision và recall thay đổi thế nào.
