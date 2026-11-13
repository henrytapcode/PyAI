Hoàn thành hàm `confusion_counts(y_true, y_pred)` bằng cách thay các ô trống `___` để đếm True Positive, False Positive, False Negative và True Negative cho mảng nhị phân `0`/`1`. Viết code bên trong hàm và `return` dictionary chứa các số `int` Python thuần.

**Ví dụ**

```python
y_true = np.array([1, 1, 0, 0])
y_pred = np.array([1, 0, 1, 0])
confusion_counts(y_true, y_pred)
# {'tp': 1, 'fp': 1, 'fn': 1, 'tn': 1}
```

**Quy tắc**
- Thay mọi ô `___` bằng phép so sánh boolean của NumPy (`&`) và `.sum()`.
- Chuyển mọi giá trị đếm sang `int` thuần của Python (không để scalar NumPy).
- Trả về dictionary có đủ bốn khóa `"tp"`, `"fp"`, `"fn"`, `"tn"` và không làm thay đổi `y_true` hay `y_pred`.
