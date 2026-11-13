Viết hai hàm `accuracy(preds, labels)` và `best_threshold(scores, labels)` để đánh giá và chọn ngưỡng tốt nhất cho bộ phân loại nhị phân. Hãy viết code bên trong từng hàm và `return` kết quả.

**Ví dụ**

```python
scores = np.array([0.1, 0.4, 0.7, 0.9])
labels = np.array([0, 0, 1, 1])
accuracy(np.array([0, 1, 1, 1]), labels)  # 0.75
best_threshold(scores, labels)            # (0.7, 1.0)
```

**Quy tắc**

- `accuracy(preds, labels)` trả về tỉ lệ phần tử `preds == labels` dưới dạng `float` Python, hoặc `0.0` nếu mảng rỗng.
- `best_threshold(scores, labels)` thử từng giá trị **khác nhau** trong `scores` làm ngưỡng `t`, đoán `1` nếu `score >= t` và `0` nếu nhỏ hơn.
- Trả về `(best_t, best_acc)` với cả hai phần tử đều là `float` chuẩn của Python (`type(...) is float`), trong đó `best_acc` làm tròn 3 chữ số thập phân.
- Nếu nhiều ngưỡng có cùng accuracy cao nhất, chọn ngưỡng `t` **nhỏ nhất**.
- Không sửa trực tiếp các mảng `preds`, `scores` hoặc `labels`.
