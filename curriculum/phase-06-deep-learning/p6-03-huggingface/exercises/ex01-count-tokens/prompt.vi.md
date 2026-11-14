Hãy điền vào các chỗ trống trong hàm `count_tokens(texts)` để trả về số lượng token không tính token đặc biệt (bỏ qua `[CLS]` và `[SEP]`) cho từng chuỗi trong `texts`, dùng `tokenizer` đã được nạp sẵn ở đầu file.

Hãy viết code bên trong hàm và `return` kết quả.

**Ví dụ**

```python
count_tokens(["Great!", "Chatbot logs!"])  # [2, 4]
count_tokens([""])                         # [0]
count_tokens([])                           # []
```

**Quy tắc**

- Không tính hai token đặc biệt `[CLS]` và `[SEP]`.
- Mọi phần tử trong list trả về phải có kiểu `int` chuẩn của Python.
- Chuỗi rỗng `""` cho ra `0` token, và danh sách rỗng `[]` trả về `[]`.
