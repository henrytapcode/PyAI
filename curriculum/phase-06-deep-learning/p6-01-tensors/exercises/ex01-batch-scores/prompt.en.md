Replace the `___` blanks in `score_batch(features, weights, bias)` so it scores a 2D batch of feature vectors against `weights` and `bias`, returning a Python `list` of rounded floats. Write your code inside the function and `return` the answer.

**Example**

```python
features = torch.tensor([[1.0, 2.0], [3.0, 1.0]])
weights = torch.tensor([0.5, 1.0])
score_batch(features, weights, bias=0.5)  # [3.0, 3.0]
```

**Rules**

- Combine `features` and `weights` using `@`, then add `bias`.
- Convert the score tensor with `.tolist()` and round each item to 3 decimal places.
- Return a Python `list` of built-in `float` values, not a tensor.
- Do not modify `features` or `weights` in place.
