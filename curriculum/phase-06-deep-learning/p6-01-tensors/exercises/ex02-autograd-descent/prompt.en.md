Implement two functions using PyTorch autograd for the model `y = w * x` with MSE loss `((w * xs - ys) ** 2).mean()`:

1. `slope_at(w_value, xs, ys)` computes the gradient of the MSE loss with respect to `w` at `w_value` using autograd and returns it rounded to 3 decimal places as a Python `float`.
2. `fit_slope(xs, ys, lr, steps)` starts from `w = 0.0`, runs `steps` gradient descent updates using autograd (`torch.no_grad()` and `.grad.zero_()`), and returns the final `w` rounded to 3 decimal places as a Python `float`.

Write your code inside each function and `return` the answer.

**Example**

```python
xs = torch.tensor([1.0, 2.0, 3.0, 4.0])
ys = torch.tensor([3.0, 6.0, 9.0, 12.0])
slope_at(1.0, xs, ys)             # -30.0
fit_slope(xs, ys, lr=0.05, steps=20)  # 3.0
```

**Rules**

- Return built-in Python `float` values (`type(result) is float`), never tensors.
- `slope_at` must give the same answer if called twice with the same inputs.
- When `steps == 0`, `fit_slope` must return `0.0`.
- Do not modify `xs` or `ys` in place.
