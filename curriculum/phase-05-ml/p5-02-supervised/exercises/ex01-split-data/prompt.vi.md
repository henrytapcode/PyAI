Thay các chỗ trống `___` trong hàm `split_data(X, y, test_ratio, seed)` để xáo chỉ số hàng một cách lặp lại được và trả về `(X_train, X_test, y_train, y_test)`. Hãy viết code bên trong hàm và `return` bốn mảng đó.

**Ví dụ**

```python
X = np.arange(10).reshape(5, 2)
y = np.arange(5)
X_train, X_test, y_train, y_test = split_data(X, y, test_ratio=0.2, seed=42)
# len(X_train) == 4, len(X_test) == 1, len(y_train) == 4, len(y_test) == 1
```

**Quy tắc**

- Khởi tạo bộ sinh ngẫu nhiên bằng `np.random.default_rng(seed)` và xáo vị trí bằng `rng.permutation(len(X))`.
- Tính `n_test = int(round(len(X) * test_ratio))`.
- Lấy `n_test` chỉ số **đầu tiên** của `idx` làm tập test, phần chỉ số còn lại làm tập train.
- Giữ `X` và `y` khớp từng hàng sau khi xáo và không sửa trực tiếp các mảng đầu vào.
