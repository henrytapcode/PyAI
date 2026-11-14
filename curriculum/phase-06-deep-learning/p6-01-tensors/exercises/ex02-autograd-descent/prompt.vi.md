Viết hai hàm dùng PyTorch autograd cho mô hình `y = w * x` với MSE loss `((w * xs - ys) ** 2).mean()`:

1. `slope_at(w_value, xs, ys)` tính gradient của MSE loss theo `w` tại `w_value` bằng autograd và trả về số `float` Python làm tròn 3 chữ số thập phân.
2. `fit_slope(xs, ys, lr, steps)` bắt đầu từ `w = 0.0`, chạy `steps` bước gradient descent bằng autograd (dùng `torch.no_grad()` và `.grad.zero_()`), rồi trả về `w` cuối cùng làm tròn 3 chữ số thập phân dưới dạng `float` Python.

Hãy viết code bên trong từng hàm và `return` kết quả.

**Ví dụ**

```python
xs = torch.tensor([1.0, 2.0, 3.0, 4.0])
ys = torch.tensor([3.0, 6.0, 9.0, 12.0])
slope_at(1.0, xs, ys)             # -30.0
fit_slope(xs, ys, lr=0.05, steps=20)  # 3.0
```

**Quy tắc**

- Luôn trả về `float` chuẩn của Python (`type(result) is float`), không trả về tensor.
- Gọi `slope_at` hai lần với cùng đầu vào phải cho ra cùng một kết quả.
- Khi `steps == 0`, `fit_slope` phải trả về `0.0`.
- Không sửa đổi `xs` hay `ys` tại chỗ.
