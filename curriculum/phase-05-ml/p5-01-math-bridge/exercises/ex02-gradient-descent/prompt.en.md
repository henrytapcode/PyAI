Implement two functions to fit a straight line `y = w * x + b` with gradient descent:

1. `mse(w, b, xs, ys)` returns the mean squared error `np.mean((pred - ys) ** 2)` as a Python `float`, where `pred = w * xs + b`.
2. `fit_line(xs, ys, lr, steps)` starts from `w = 0.0` and `b = 0.0`, runs `steps` gradient descent updates using the MSE gradients:
   - `grad_w = np.mean(2 * (pred - ys) * xs)`
   - `grad_b = np.mean(2 * (pred - ys))`
   and returns `(round(float(w), 3), round(float(b), 3))`.

Write your code inside the functions and `return` the answers.

**Example**

```python
xs = np.array([1.0, 2.0, 3.0, 4.0])
ys = np.array([3.0, 5.0, 7.0, 9.0])

mse(2.0, 1.0, xs, ys)              # 0.0
fit_line(xs, ys, lr=0.05, steps=250)  # approx (2.0, 1.0)
```

**Rules**

- `mse` must return a built-in Python `float`.
- `fit_line` must start at `w = 0.0`, `b = 0.0` and return `(0.0, 0.0)` when `steps == 0`.
- `fit_line` must return a tuple of two built-in Python `float`s rounded to 3 decimal places.
- Do not modify `xs` or `ys` in place.
