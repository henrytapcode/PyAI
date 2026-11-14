Implement the training, evaluation, and prediction loop for BERT-Tiny: `accuracy`, `fine_tune`, and `predict`. The pinned `tokenizer` and helper `load_model()` are already provided at the top of the file; write your code inside each function and `return` the result.

**Example**

```python
model = load_model()
losses = fine_tune(model, train_texts, train_labels, lr=5e-4, epochs=10)
acc = accuracy(model, val_texts, val_labels)   # e.g. 1.0
labels = predict(model, ["App crashed", "Charged twice"])  # ["bug", "billing"]
```

**Rules**

- `accuracy(model, texts, labels)`:
  - Switch `model.eval()` and run inside `with torch.no_grad():`.
  - Tokenize `texts` with `padding=True, truncation=True, return_tensors="pt"`.
  - Return the fraction of exact matches rounded to 3 decimal places as a built-in Python `float`.
- `fine_tune(model, texts, labels, lr, epochs)`:
  - If `epochs <= 0`, return `[]` immediately without modifying model weights.
  - Run full-batch training using `torch.optim.AdamW(model.parameters(), lr=lr)` with `model.train()` and `out = model(**batch, labels=y)` (`y` has `dtype=torch.int64`).
  - Return a `list[float]` of per-epoch training losses, each rounded to 4 decimal places as a built-in Python `float`.
- `predict(model, texts)`:
  - Switch `model.eval()` and run inside `with torch.no_grad():`.
  - Map predicted class indices to text labels (`"bug"` / `"billing"`) via `model.config.id2label`.
