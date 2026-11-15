Implement three data-preparation helpers for the ticket classifier: `split_data`, `encode`, and `class_counts`. The BERT-Tiny `tokenizer` is already loaded at the top of the file; write your code inside each function and `return` the result.

**Example**

```python
train_x, train_y, val_x, val_y, test_x, test_y = split_data(
    texts, labels, val_frac=0.2, test_frac=0.2, seed=27
)
batch = encode(["App crashes", "Card charged twice"], max_length=16)
# {"input_ids": <shape (2, 5)>, "attention_mask": <shape (2, 5)>}
class_counts([0, 1, 0])  # {0: 2, 1: 1}
```

**Rules**

- In `split_data(texts, labels, val_frac, test_frac, seed)`:
  - Shuffle indices with `torch.randperm(len(texts), generator=torch.Generator().manual_seed(seed)).tolist()`.
  - Compute `n_val = int(len(texts) * val_frac)`, `n_test = int(len(texts) * test_frac)`, and `n_train = len(texts) - n_val - n_test`.
  - Keep every `(text, label)` pair aligned and return `(train_texts, train_labels, val_texts, val_labels, test_texts, test_labels)`.
- In `encode(texts, max_length)`:
  - Use the module-level `tokenizer` with `padding=True`, `truncation=True`, `max_length=max_length`, and `return_tensors="pt"`.
  - Return a dictionary containing `"input_ids"` and `"attention_mask"` tensors.
- In `class_counts(labels)`:
  - Return a `dict[int, int]` mapping each label integer to how many times it appears (`{}` for an empty list).
