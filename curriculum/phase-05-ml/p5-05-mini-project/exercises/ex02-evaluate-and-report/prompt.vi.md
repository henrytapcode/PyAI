Viết hai hàm—`evaluate_models(X, y, seed)` và `write_report(results, n_test)`—để so sánh các bộ phân loại bằng cross-validation 5 fold có phân tầng và xuất báo cáo tóm tắt trung thực. Viết code bên trong từng hàm và `return` kết quả tương ứng.

**Ví dụ**

```python
results = {"baseline": (0.0, 0.0), "logreg": (0.709, 0.092), "tree": (0.701, 0.14)}
write_report(results, n_test=58)
```

Trả về:

```text
[
    "baseline F1: 0.000 +/- 0.000",
    "logreg F1: 0.709 +/- 0.092",
    "tree F1: 0.701 +/- 0.140",
    "best: logreg",
    "test size: 58",
    "warning: logreg and tree differ by less than one std",
]
```

**Quy tắc**

- `evaluate_models(X, y, seed)`:
  - Chạy `StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)` 5 fold trên **toàn bộ** `X, y` đưa vào (người gọi đã tách riêng tập test trước đó).
  - Đánh giá đúng ba mô hình theo thứ tự:
    - `"baseline"`: `DummyClassifier(strategy="most_frequent")`
    - `"logreg"`: `make_pipeline(StandardScaler(), LogisticRegression())`
    - `"tree"`: `DecisionTreeClassifier(max_depth=3, random_state=0)`
  - Chấm điểm F1 bằng `make_scorer(f1_score, zero_division=0)` (hoặc cách tương đương sạch warning) để điểm baseline `0.0` không phát sinh cảnh báo.
  - Trả về `{name: (mean, std)}` với cả hai số làm tròn `3` chữ số thập phân ở kiểu `float` Python. Không sửa đổi `X` hay `y`.
- `write_report(results, n_test)`:
  - Ném `ValueError` nếu `results` không có mô hình nào ngoài `"baseline"` (rỗng hoặc chỉ có `"baseline"`).
  - Tạo một dòng cho mỗi mô hình theo đúng thứ tự của `results`: `f"{name} F1: {mean:.3f} +/- {std:.3f}"`.
  - Thêm dòng `f"best: {best_name}"` là tên mô hình (không tính `"baseline"`) có `mean` cao nhất (hòa thì chọn theo thứ tự bảng chữ cái).
  - Thêm dòng `f"test size: {n_test}"`.
  - Nếu có ít nhất hai mô hình ngoài `"baseline"`, gọi `a` là mô hình tốt nhất và `b` là mô hình tốt nhì (xếp theo `mean` giảm dần, hòa theo chữ cái). Khi `abs(mean_a - mean_b) < max(std_a, std_b)` (nhỏ hơn nghiêm ngặt `<`), thêm dòng `f"warning: {a} and {b} differ by less than one std"`.
  - Không sửa đổi `results`.
