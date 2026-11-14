Hãy cài đặt hai hàm phân loại phản hồi bằng `tokenizer` và `model` đã được nạp sẵn ở đầu file:

1. `classify(texts: list[str]) -> list[tuple[str, float]]`: tokenize `texts` với `padding=True`, `truncation=True` và `return_tensors="pt"`, chạy suy đoán trong `model.eval()` và `with torch.no_grad():`, tính `torch.softmax(..., dim=1)` cùng `argmax(dim=1)`, rồi đổi nhãn qua `model.config.id2label`. Trả về `(label, round(score, 3))` cho mỗi câu, với `score` là `float` Python. **Không** dùng `pipeline`.
2. `negatives(texts: list[str], threshold: float) -> list[str]`: lọc ra các câu được dự đoán `"NEGATIVE"` có `score >= threshold`, giữ nguyên thứ tự ban đầu.

Hãy viết code bên trong hai hàm và `return` kết quả.

**Ví dụ**

```python
classify(["Fast and helpful!", "Broken link again."])
# [("POSITIVE", 1.0), ("NEGATIVE", 0.999)]

negatives(["Fast and helpful!", "Broken link again."], threshold=0.95)
# ["Broken link again."]
```

**Quy tắc**

- Cả hai hàm phải xử lý sạch danh sách rỗng `[]` bằng cách trả về `[]`.
- Trong `classify`, không gọi `transformers.pipeline`; tự tính softmax, argmax và ánh xạ nhãn trực tiếp từ `model`.
- Mỗi `score` trong `classify` phải là kiểu `float` chuẩn của Python nằm trong `[0.0, 1.0]` và làm tròn 3 chữ số thập phân.
