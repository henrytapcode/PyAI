Từ dịch vụ RAG đã chạy sẵn trong `starter.py`, hãy thêm bộ nhớ đệm TTL trong RAM và theo dõi độ trễ cùng chi phí theo từng request qua route `GET /metrics`. Viết code bên trong `create_app` (cùng các hàm hoặc class phụ nếu cần) và trả về đối tượng `FastAPI`.

**Ví dụ**

```text
GET  /metrics (before any /ask)                        -> 200 {"requests": 0, "cache_hit_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds"], "usage": {...}, "cached": false}
POST /ask {"question": "  How long   do refunds take?"}-> 200 {"answer": "...", "sources": ["refunds"], "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cached": true}
GET  /metrics                                          -> 200 {"requests": 2, "cache_hit_rate": 0.5, "p95_ms": ..., "total_cost": ...}
```

**Quy tắc**
- Chữ ký hàm: `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015) -> FastAPI`, trong đó `clock` là một callable không tham số trả về giây (không gọi các hàm thời gian thật của `time.*`).
- Thêm trường `"cached": bool` vào mọi phản hồi của `POST /ask`.
- Cache key phải phụ thuộc vào câu hỏi đã chuẩn hóa (bỏ khoảng trắng đầu/cuối và gộp khoảng trắng liên tiếp) **và** `top_k`.
- Mục cache chỉ hợp lệ khi `clock() < expires_at` (khi `clock() >= expires_at` thì tính là trượt cache). Khi trúng cache, không gọi `client.embed` hay `client.chat`, và trả `usage: {"prompt_tokens": 0, "completion_tokens": 0}`.
- **Có cache cả câu từ chối**: nếu truy xuất không có tài liệu nào đạt `min_score`, vẫn lưu câu từ chối vào cache để lần hỏi lặp lại trong hạn `cache_ttl` trả `cached: true`.
- Với mỗi request `POST /ask` hợp lệ (trúng cache, trượt cache hoặc từ chối), ghi lại `latency_ms = (clock_sau - clock_trước) * 1000`, `cost` tính theo `price_in_per_1k` và `price_out_per_1k` (`0.0` khi trúng cache), và `cached`.
- `GET /metrics` trả về `{"requests": int, "cache_hit_rate": float, "p95_ms": float, "total_cost": float}`, trong đó `p95_ms` tính theo nearest-rank và `total_cost` làm tròn 6 chữ số thập phân (trả về `0` / `0.0` nếu chưa có request nào).
