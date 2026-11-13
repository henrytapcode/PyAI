Một bộ phân loại trả về mảng 2D `probs`, trong đó mỗi hàng là một mẫu và mỗi cột là xác suất của một lớp. Hãy viết `predicted_labels(probs, labels, threshold)` để chọn lớp có xác suất cao nhất cho từng hàng, hoặc trả `"unsure"` nếu xác suất đó nhỏ hơn `threshold`. Đặt code bên trong hàm và `return` kết quả dưới dạng một `list` các chuỗi Python.

**Ví dụ**

```python
probs = np.array([[0.10, 0.90], [0.55, 0.45]])
predicted_labels(probs, ["no", "yes"], 0.6)
# -> ["yes", "unsure"]
```

**Quy tắc**
- Dùng `probs.argmax(axis=1)` (hoặc `argmax` theo từng hàng) để khi hòa điểm sẽ chọn chỉ số lớp đầu tiên.
- Nếu xác suất cao nhất đúng bằng `threshold` (`prob >= threshold`), vẫn nhận nhãn dự đoán.
- Trả về `list[str]` thuần của Python, không trả về mảng NumPy.
- Không sửa `probs` hay `labels`.
