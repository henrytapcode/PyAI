Từ dịch vụ RAG đã chạy sẵn trong `starter.py`, hãy thêm bộ nhớ đệm TTL trong RAM, nhánh xử lý lỗi `RateLimitError` (`503`) và theo dõi độ trễ, chi phí cùng tỉ lệ lỗi qua route `GET /metrics`. Viết code bên trong `create_app` (cùng các hàm hoặc class phụ nếu cần) và trả về đối tượng `FastAPI`.

**Ví dụ**

```text
GET  /metrics (before any /ask)                        -> 200 {"requests": 0, "cache_hit_rate": 0.0, "error_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
POST /ask (when model raises RateLimitError)           -> 503 {"detail": "model busy, retry later"}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds"], "usage": {...}, "cached": false}
POST /ask {"question": "  How long   do refunds take?"}-> 200 {"answer": "...", "sources": ["refunds"], "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cached": true}
GET  /metrics?last=2                                   -> 200 {"requests": 2, "cache_hit_rate": 0.5, "error_rate": 0.0, "p95_ms": ..., "total_cost": ...}
```

**Quy tắc**
- Chữ ký hàm: `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015) -> FastAPI`, trong đó `clock` là một callable không tham số trả về giây (không gọi các hàm thời gian thật của `time.*`).
- Thêm trường `"cached": bool` vào mọi phản hồi thành công của `POST /ask`.
- Cache key phải phụ thuộc vào câu hỏi đã chuẩn hóa (bỏ khoảng trắng đầu/cuối và gộp khoảng trắng liên tiếp) **và** `top_k`.
- Mục cache chỉ hợp lệ khi `clock() < expires_at` (khi `clock() >= expires_at` thì tính là trượt cache). Khi trúng cache, không gọi `client.embed` hay `client.chat`, và trả `usage: {"prompt_tokens": 0, "completion_tokens": 0}`.
- **Có cache cả câu từ chối**: nếu truy xuất không có tài liệu nào đạt `min_score`, vẫn lưu câu từ chối vào cache để lần hỏi lặp lại trong hạn `cache_ttl` trả `cached: true`.
- **Xử lý `RateLimitError`**: nếu `client.embed` (lúc hỏi) hoặc `client.chat` ném `RateLimitError` (`from pyai_llm import RateLimitError`), **không** lưu vào cache, vẫn ghi nhận bản ghi với `status="error"`, `cost=0.0`, `latency_ms` đo bình thường, rồi ném `HTTPException(status_code=503, detail="model busy, retry later")`. Các request `POST /ask` hợp lệ khác ghi `status="ok"`.
- Với mỗi request `POST /ask` hợp lệ (trúng cache, trượt cache, từ chối hoặc lỗi), ghi lại `latency_ms = (clock_sau - clock_trước) * 1000`, `cost` tính theo `price_in_per_1k` và `price_out_per_1k` (`0.0` khi trúng cache, từ chối hoặc lỗi), `cached` và `status`.
- `GET /metrics` nhận tham số truy vấn tùy chọn `last: int | None` (`>= 1`, trả `422` khi `last=0`). Dùng `Query` của `fastapi` cho tham số truy vấn giống như dùng `Field` cho body—ví dụ `last: int | None = Query(default=None, ge=1)`—FastAPI sẽ tự động trả về `422` khi vi phạm. Khi có `last=N`, mọi chỉ số chỉ tính trên `N` bản ghi cuối cùng; ngược lại tính trên toàn bộ. Trả về đúng thứ tự khóa: `requests`, `cache_hit_rate`, `error_rate`, `p95_ms`, `total_cost` (`p95_ms` tính theo nearest-rank, `total_cost` làm tròn 6 chữ số thập phân, trả `0` / `0.0` khi rỗng).
