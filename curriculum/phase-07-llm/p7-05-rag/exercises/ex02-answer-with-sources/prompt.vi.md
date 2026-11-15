Cài đặt hàm `answer_with_sources(question, chunks, client, k=2, min_score=0.2)` trong `starter.py` để truy xuất top-`k` chunk, dựng prompt có căn cứ, gọi `client.chat()` và trả về câu trả lời kèm danh sách nguồn hợp lệ.

Viết code bên trong hàm và `return` dictionary dạng `{"answer": str, "sources": list[str]}`.

## Ví dụ

```python
chunks = [
    {"text": "Refunds are issued within 30 days of purchase.", "source": "refunds.md"},
    {"text": "Standard shipping delivers in five days.", "source": "shipping.md"},
]
answer_with_sources("How many days do refunds take?", chunks, FakeLLM(embed_dim=256))
# -> {"answer": "Refunds are issued within 30 days of purchase. [1]", "sources": ["refunds.md"]}
```

## Quy tắc

- Mỗi phần tử trong `chunks` có dạng `{"text": str, "source": str}`.
- Embed toàn bộ văn bản chunk trong một lần gọi `client.embed(...)` và embed `[question]` ở lần gọi thứ hai (tổng cộng 2 lần gọi `embed`; gộp cả hai thành 1 lần gọi `embed` cũng được chấp nhận).
- Xếp hạng chunk bằng tích vô hướng (`doc_matrix @ q_vec`) với `np.argsort(-scores, kind="stable")[:k]`.
- Nếu `chunks` rỗng, `k <= 0`, hoặc điểm cao nhất `< min_score`, trả về `{"answer": "I don't know.", "sources": []}` mà **không** gọi `client.chat()`.
- Định dạng message `system` gồm phần hướng dẫn, theo sau là một dòng đúng bằng `Context:` và các dòng `[1] <text>`, `[2] <text>`, ... theo đúng thứ tự top-`k`; truyền `question` trong một message `user` riêng.
- Tách các trích dẫn `[n]` trong `answer`, bỏ qua các số ngoài phạm vi (`n < 1` hoặc `n > len(hits)`), và ánh xạ các số hợp lệ sang `source` không trùng lặp, giữ nguyên thứ tự xuất hiện đầu tiên.
