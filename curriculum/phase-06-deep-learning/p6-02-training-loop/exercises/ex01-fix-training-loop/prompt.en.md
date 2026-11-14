`train(model, xs, ys, lr, epochs)` runs without crashing, but produces the wrong result because it has **2 bugs**. Find and fix both bugs inside the function, and `return` the list of epoch losses.

**Example**

```python
torch.manual_seed(0)
model = nn.Linear(1, 1)
xs = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
ys = 2.0 * xs + 1.0
losses = train(model, xs, ys, lr=0.05, epochs=30)
# len(losses) == 30, every item is a Python float, and losses[-1] < 0.05
```

**Rules**

- Return a Python `list` of length `epochs`.
- Each entry must be a built-in Python `float` rounded to 4 decimal places (`round(loss.item(), 4)`), not a tensor.
- Keep using `nn.MSELoss()` and `torch.optim.SGD(model.parameters(), lr=lr)`.
- Do not modify `xs` or `ys` in place.
