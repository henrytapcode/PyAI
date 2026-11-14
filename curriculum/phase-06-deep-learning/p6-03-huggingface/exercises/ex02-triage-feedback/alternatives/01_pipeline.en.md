# Using `pipeline()` with preloaded objects

This alternative builds `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)` from the already-loaded `model` and `tokenizer` objects instead of manually calling `tokenizer(...)`, `model(**batch)`, `torch.softmax`, and `argmax`.

**When it is enough:** For quick scripts, prototypes, and standard inference where default batching and softmax scores are all you need, `pipeline()` is shorter and leaves fewer places to make shape or `no_grad()` mistakes.

**When to do it step by step:** Whenever you need raw logits (for threshold calibration or loss calculation), custom padding/truncation control, or a training loop to fine-tune the model weights (`p6-04-fine-tune`), write the explicit tokenizer + model steps from `solution.py`.
