Implement two sentiment-triage helpers using the preloaded `tokenizer` and `model`:

1. `classify(texts: list[str]) -> list[tuple[str, float]]`: tokenize `texts` with `padding=True`, `truncation=True`, and `return_tensors="pt"`, run inference under `model.eval()` and `with torch.no_grad():`, apply `torch.softmax(..., dim=1)` and `argmax(dim=1)`, and map each prediction via `model.config.id2label`. Return `(label, round(score, 3))` for each sentence with `score` as a Python `float`. Do **not** use `pipeline`.
2. `negatives(texts: list[str], threshold: float) -> list[str]`: return only the sentences predicted as `"NEGATIVE"` with `score >= threshold`, preserving the original order.

Write your code inside the functions and `return` the answer.

**Example**

```python
classify(["Fast and helpful!", "Broken link again."])
# [("POSITIVE", 1.0), ("NEGATIVE", 0.999)]

negatives(["Fast and helpful!", "Broken link again."], threshold=0.95)
# ["Broken link again."]
```

**Rules**

- Handle an empty list `[]` cleanly by returning `[]` in both functions.
- In `classify`, do not call `transformers.pipeline`; compute softmax, argmax, and labels directly from `model`.
- Each score in `classify` must be a built-in Python `float` in `[0.0, 1.0]` rounded to 3 decimal places.
