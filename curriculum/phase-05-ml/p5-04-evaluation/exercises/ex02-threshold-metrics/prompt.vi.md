Hãy tự cài đặt hai hàm đánh giá từ đầu mà không gọi `sklearn.metrics`:

1. `precision_recall_f1(y_true, y_pred)` tính precision, recall và F1 từ các ô đếm (`tp`, `fp`, `fn`), trả về `0.0` cho chỉ số nào có mẫu số bằng 0, và chỉ làm tròn 3 chữ số thập phân ở bước trả kết quả.
2. `threshold_for_recall(probs, y_true, thresholds, min_recall)` dự đoán `1` khi `probs >= t` và trả về ngưỡng **lớn nhất** trong `thresholds` có recall đạt ít nhất `min_recall`, hoặc `None` nếu không có ngưỡng nào đạt.

Viết code bên trong hai hàm và `return` kết quả.

**Ví dụ**

```python
precision_recall_f1(np.array([1, 1, 1, 0, 0]), np.array([1, 0, 0, 0, 0]))
# (1.0, 0.333, 0.5)

threshold_for_recall(
    np.array([0.8, 0.4, 0.2]),
    np.array([1, 1, 0]),
    thresholds=[0.3, 0.5, 0.7],
    min_recall=0.8,
)
# 0.3
```

**Quy tắc**
- Trong `precision_recall_f1`, tính F1 từ precision và recall chưa làm tròn (`0.0` khi `precision + recall == 0`), rồi trả về tuple gồm ba `float` Python thuần làm tròn 3 chữ số thập phân.
- Không gọi `sklearn.metrics` trong hai hàm.
- Danh sách `thresholds` có thể không theo thứ tự; hãy trả về ngưỡng lớn nhất đạt yêu cầu dưới dạng `float` Python, hoặc `None` nếu không ngưỡng nào đạt `min_recall`.
- Không làm thay đổi mảng đầu vào hay danh sách `thresholds`.
