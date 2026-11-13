Viết hai hàm để khớp một đường thẳng `y = w * x + b` bằng gradient descent:

1. `mse(w, b, xs, ys)` trả về mean squared error `np.mean((pred - ys) ** 2)` dưới dạng `float` Python, với `pred = w * xs + b`.
2. `fit_line(xs, ys, lr, steps)` bắt đầu từ `w = 0.0` và `b = 0.0`, lặp `steps` bước gradient descent với công thức gradient của MSE:
   - `grad_w = np.mean(2 * (pred - ys) * xs)`
   - `grad_b = np.mean(2 * (pred - ys))`
   rồi trả về `(round(float(w), 3), round(float(b), 3))`.

Hãy viết code bên trong hai hàm và `return` đáp án.

**Ví dụ**

```python
xs = np.array([1.0, 2.0, 3.0, 4.0])
ys = np.array([3.0, 5.0, 7.0, 9.0])

mse(2.0, 1.0, xs, ys)              # 0.0
fit_line(xs, ys, lr=0.05, steps=250)  # xấp xỉ (2.0, 1.0)
```

**Quy tắc**

- `mse` phải trả về đúng kiểu `float` của Python.
- `fit_line` phải bắt đầu từ `w = 0.0`, `b = 0.0` và trả về `(0.0, 0.0)` khi `steps == 0`.
- `fit_line` phải trả về tuple gồm hai `float` Python đã làm tròn 3 chữ số thập phân.
- Không sửa đổi trực tiếp `xs` hay `ys`.
