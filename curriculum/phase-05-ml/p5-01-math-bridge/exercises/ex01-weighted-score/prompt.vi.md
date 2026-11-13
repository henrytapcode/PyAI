Thay các ô `___` trong hàm `weighted_score(features, weights, bias)` để tính điểm có trọng số của một vector feature và trả về kết quả dạng `float` Python. Hãy viết code bên trong hàm và `return` đáp án.

**Ví dụ**

```python
weighted_score(np.array([2.0, 3.0]), np.array([0.5, 1.0]), 0.5)  # 4.5
```

**Quy tắc**

- Kết hợp `features` và `weights` bằng tích vô hướng, sau đó cộng thêm `bias`.
- Trả về đúng kiểu `float` của Python (`type(result) is float`), không phải scalar NumPy.
- Không sửa đổi trực tiếp `features` hay `weights`.
