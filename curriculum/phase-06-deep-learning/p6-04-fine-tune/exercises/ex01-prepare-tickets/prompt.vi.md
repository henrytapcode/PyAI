Cài đặt ba hàm chuẩn bị dữ liệu cho bộ phân loại ticket: `split_data`, `encode` và `class_counts`. `tokenizer` của BERT-Tiny đã được nạp sẵn ở đầu file; hãy viết code bên trong từng hàm và `return` kết quả.

**Ví dụ**

```python
train_x, train_y, val_x, val_y, test_x, test_y = split_data(
    texts, labels, val_frac=0.2, test_frac=0.2, seed=27
)
batch = encode(["App crashes", "Card charged twice"], max_length=16)
# {"input_ids": <shape (2, 6)>, "attention_mask": <shape (2, 6)>}
class_counts([0, 1, 0])  # {0: 2, 1: 1}
```

**Quy tắc**

- Trong `split_data(texts, labels, val_frac, test_frac, seed)`:
  - Xáo chỉ số bằng `torch.randperm(len(texts), generator=torch.Generator().manual_seed(seed)).tolist()`.
  - Tính `n_val = int(len(texts) * val_frac)`, `n_test = int(len(texts) * test_frac)` và `n_train = len(texts) - n_val - n_test`.
  - Giữ đúng từng cặp `(text, label)` và trả về `(train_texts, train_labels, val_texts, val_labels, test_texts, test_labels)`.
- Trong `encode(texts, max_length)`:
  - Dùng `tokenizer` có sẵn ở mức module với `padding=True`, `truncation=True`, `max_length=max_length` và `return_tensors="pt"`.
  - Trả về dict chứa các tensor `"input_ids"` và `"attention_mask"`.
- Trong `class_counts(labels)`:
  - Trả về `dict[int, int]` ánh xạ mỗi nhãn số nguyên tới số lần xuất hiện của nó (`{}` nếu danh sách rỗng).
