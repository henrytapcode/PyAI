Hãy thay các ô `___` trong hàm `train_and_score(X, y, seed)` để chia dữ liệu 75/25 có `stratify`, dựng pipeline gồm `StandardScaler` và `LogisticRegression`, huấn luyện trên tập train rồi trả về accuracy trên tập test đã làm tròn. Viết code bên trong hàm và `return` một `float` của Python.

**Ví dụ**

```python
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
score = train_and_score(X, y, seed=42)
# 0.921
```

**Quy tắc**

- Dùng `train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)`.
- Tạo pipeline bằng `make_pipeline(StandardScaler(), LogisticRegression())`.
- Chỉ gọi `.fit` trên `(X_train, y_train)` và chấm điểm trên `(X_test, y_test)`.
- Trả về `round(float(score), 3)` kiểu `float` Python thuần, không làm thay đổi mảng `X` hay `y` đầu vào.
