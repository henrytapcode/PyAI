Cài đặt hàm `top_k(query, docs, client, k=2, min_score=0.0)` trong `starter.py` để xếp hạng tài liệu theo độ tương đồng embedding và lọc bỏ các kết quả quá yếu.

Viết code của bạn bên trong thân hàm và `return` danh sách các tuple `(index, score)`.

## Ví dụ

```python
client = FakeLLM(embed_dim=256)
docs = ["cheap car rental", "fast laptop repair", "book a doctor"]
top_k("affordable automobile", docs, client, k=1, min_score=0.3)
# -> [(0, 0.816)]
```

## Quy tắc

- Nếu `docs` rỗng (hoặc `k <= 0`), trả về `[]` ngay lập tức và **không** gọi `client.embed(...)`.
- Embed `docs` trong một lần gọi lô duy nhất (có thể gọi `client.embed(docs)` cùng `client.embed([query])`, hoặc gộp chung một lần `client.embed([query, *docs])` — tuyệt đối không lặp để gọi `embed` cho từng tài liệu).
- Trả về danh sách `(index, score)` sắp xếp theo điểm giảm dần; nếu điểm bằng nhau thì ưu tiên `index` nhỏ hơn đứng trước.
- Làm tròn mỗi `score` đến 3 chữ số thập phân và chuyển sang `float` chuẩn của Python (không để NumPy scalar).
- Loại bỏ mọi tài liệu có điểm nhỏ hơn `min_score` (nếu bằng `min_score` thì vẫn giữ).
- Nếu `k` lớn hơn số tài liệu hiện có, trả về toàn bộ tài liệu đạt ngưỡng.
