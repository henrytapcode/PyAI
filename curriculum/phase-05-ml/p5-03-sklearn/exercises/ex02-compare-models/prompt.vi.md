Viết hai hàm để so sánh các mô hình scikit-learn ứng viên trên cùng một lần chia dữ liệu và chọn mô hình tốt nhất. Viết code bên trong từng hàm và `return` kết quả.

1. `compare_models(X, y, models, seed)`: chia dữ liệu 70/30 có `stratify` **một lần duy nhất** với `random_state=seed`, huấn luyện một bản sao mới của từng estimator trong `models` trên `(X_train, y_train)`, rồi trả về `dict[str, float]` ánh xạ tên từng mô hình (đúng thứ tự key của `models`) sang accuracy trên phần held-out làm tròn 3 chữ số thập phân.
2. `best_model(scores)`: trả về tên mô hình có điểm cao nhất; nếu hòa, chọn tên đứng trước theo thứ tự chữ cái; nếu `scores` rỗng thì ném `ValueError`. Điểm đưa vào đây là điểm trên một phần held-out để so sánh; sang `p5-04-evaluation` bạn sẽ đưa điểm cross-validation vào đúng hàm này.

**Ví dụ**

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0
)
models = {
    "logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "knn": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3)),
    "tree": DecisionTreeClassifier(max_depth=3, random_state=0),
}
scores = compare_models(X, y, models, seed=42)
# {'logreg': 0.722, 'knn': 0.833, 'tree': 0.722}
best_model(scores)
# 'knn'
```

**Quy tắc**

- Chỉ chia `(X, y)` **một lần** bằng `train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)`.
- Nhân bản từng estimator bằng `sklearn.base.clone(model)` (tạo bản sao mới chưa huấn luyện với cùng siêu tham số) trước khi `.fit(...)` để các object trong `models` vẫn ở trạng thái chưa fit.
- Trả về điểm kiểu `float` Python làm tròn 3 chữ số và giữ nguyên thứ tự key của `models`.
- Trong `best_model(scores)`, ném `ValueError` khi `scores` rỗng và xử lý hòa theo thứ tự bảng chữ cái (`"alpha"` thắng `"zeta"`).
