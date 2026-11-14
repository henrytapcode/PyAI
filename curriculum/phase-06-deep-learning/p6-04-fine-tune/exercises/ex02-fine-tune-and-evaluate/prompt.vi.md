Cài đặt vòng lặp huấn luyện, đánh giá và dự đoán cho BERT-Tiny: `accuracy`, `fine_tune` và `predict`. `tokenizer` đã ghim và hàm `load_model()` đã được cung cấp sẵn ở đầu file; hãy viết code bên trong từng hàm và `return` kết quả.

**Ví dụ**

```python
model = load_model()
losses = fine_tune(model, train_texts, train_labels, lr=5e-4, epochs=10)
acc = accuracy(model, val_texts, val_labels)   # vd 1.0
labels = predict(model, ["App crashed", "Charged twice"])  # ["bug", "billing"]
```

**Quy tắc**

- `accuracy(model, texts, labels)`:
  - Bật `model.eval()` và chạy trong `with torch.no_grad():`.
  - Tokenize `texts` với `padding=True, truncation=True, return_tensors="pt"`.
  - Trả về tỉ lệ đoán đúng làm tròn 3 chữ số thập phân với kiểu `float` thuần của Python.
- `fine_tune(model, texts, labels, lr, epochs)`:
  - Nếu `epochs <= 0`, trả ngay `[]` và không làm thay đổi trọng số của model.
  - Huấn luyện full-batch bằng `torch.optim.AdamW(model.parameters(), lr=lr)` với `model.train()` và `out = model(**batch, labels=y)` (`y` có `dtype=torch.int64`).
  - Trả về `list[float]` chứa train loss của từng epoch, mỗi giá trị làm tròn 4 chữ số thập phân với kiểu `float` thuần của Python.
- `predict(model, texts)`:
  - Bật `model.eval()` và chạy trong `with torch.no_grad():`.
  - Đổi chỉ số lớp dự đoán sang nhãn chữ (`"bug"` / `"billing"`) qua `model.config.id2label`.
