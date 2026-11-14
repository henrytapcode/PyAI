Điền vào các chỗ trống `___` trong `score_batch(features, weights, bias)` để chấm điểm một batch 2D các vector feature theo `weights` và `bias`, rồi trả về một `list` các số `float` đã làm tròn. Hãy viết code bên trong hàm và `return` kết quả.

**Ví dụ**

```python
features = torch.tensor([[1.0, 2.0], [3.0, 1.0]])
weights = torch.tensor([0.5, 1.0])
score_batch(features, weights, bias=0.5)  # [3.0, 3.0]
```

**Quy tắc**

- Kết hợp `features` và `weights` bằng toán tử `@`, sau đó cộng thêm `bias`.
- Chuyển tensor kết quả bằng `.tolist()` và làm tròn mỗi phần tử tới 3 chữ số thập phân.
- Trả về một `list` gồm các `float` chuẩn của Python, không trả về tensor.
- Không sửa đổi `features` hay `weights` tại chỗ.
