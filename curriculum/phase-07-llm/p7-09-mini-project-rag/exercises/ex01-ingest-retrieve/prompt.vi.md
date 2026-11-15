Viết hai hàm `build_index(docs, client, mode="sentence", size=8, overlap=2)` và `retrieve(index, question, client, k=2, min_score=0.2)` để nạp tài liệu FAQ thành chỉ mục embedding một lần và truy xuất top-k chunk phù hợp nhất. Viết code bên trong hai hàm và `return` kết quả.

**Ví dụ**

```python
docs = [{"source": "refunds.md", "text": "Refunds take 30 days. Keep receipt!"}]
index = build_index(docs, client, mode="sentence")
# index["chunks"] -> [
#     {"id": "refunds.md#0", "source": "refunds.md", "text": "Refunds take 30 days."},
#     {"id": "refunds.md#1", "source": "refunds.md", "text": "Keep receipt!"},
# ]
hits = retrieve(index, "How many days for refunds?", client, k=2, min_score=0.2)
# hits[0] -> {"id": "refunds.md#0", "source": "refunds.md", "text": "Refunds take 30 days.", "score": ...}
```

**Quy tắc**

- Trong `build_index`:
  - Chỉ chấp nhận `mode="sentence"` hoặc `mode="words"`; mọi giá trị `mode` khác phải raise `ValueError`.
  - Quy tắc tách câu (`mode="sentence"`): `.strip()` văn bản `doc["text"]`; nếu không rỗng, tách bằng `re.split(r"(?<=[.!?])\s+", ...)`, `.strip()` từng đoạn và bỏ đoạn rỗng. Ví dụ `"Refunds take 30 days. Keep receipt!"` tách thành `["Refunds take 30 days.", "Keep receipt!"]`.
  - Quy tắc cửa sổ từ (`mode="words"`): raise `ValueError` nếu `size <= 0`, `overlap < 0` hoặc `overlap >= size`. Tách bằng `.split()`, trượt cửa sổ `size` từ với bước nhảy `size - overlap`, và dừng khi `i + size >= len(words)`.
  - Bỏ qua tài liệu/chunk rỗng và đánh ID `f"{doc['source']}#{n}"` bắt đầu từ `0` cho mỗi `source`.
  - Gọi `client.embed(...)` **tối đa một lần** (đúng một lần cho toàn bộ chunk khi có ít nhất 1 chunk; không gọi nếu không có chunk nào).
  - Trả về `{"chunks": chunks, "vectors": vectors}` mà không làm thay đổi `docs`.
- Trong `retrieve`:
  - Trả về `[]` ngay nếu `index["chunks"]` rỗng hoặc `k <= 0`.
  - Embed `[question]`, tính độ tương đồng với `index["vectors"]`, xếp hạng giảm dần ổn định, lấy top `k`, và loại bỏ các chunk có `score < min_score`.
  - Trả về danh sách dict gồm các khóa `"id"`, `"source"`, `"text"` và `"score"` làm tròn bằng `round(float(score), 3)`.
