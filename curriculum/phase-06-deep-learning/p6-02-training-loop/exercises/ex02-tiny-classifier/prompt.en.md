Implement a small PyTorch classifier and an evaluation helper:

1. `TinyClassifier(in_features, hidden, classes)` subclasses `nn.Module` and chains `nn.Linear(in_features, hidden)` -> `nn.ReLU()` -> `nn.Linear(hidden, classes)` in `forward(self, x)` to return raw logits of shape `(N, classes)`.
2. `accuracy(model, xs, ys)` switches the model with `model.eval()`, runs inference inside `with torch.no_grad():`, and returns the fraction of correct predictions rounded to 3 decimal places as a Python `float`.

Write your code inside the class and function, and `return` the answer.

**Example**

```python
torch.manual_seed(0)
clf = TinyClassifier(in_features=2, hidden=8, classes=3)
logits = clf(torch.randn(5, 2))  # shape (5, 3)
acc = accuracy(clf, torch.randn(10, 2), torch.zeros(10, dtype=torch.int64))
```

**Rules**

- Call `super().__init__()` inside `TinyClassifier.__init__`.
- `TinyClassifier.forward` must return raw logits (do not apply softmax).
- `accuracy` must call `model.eval()`, wrap inference in `with torch.no_grad():`, and return a built-in Python `float` in `[0.0, 1.0]`.
- Do not modify `xs` or `ys` in place.
