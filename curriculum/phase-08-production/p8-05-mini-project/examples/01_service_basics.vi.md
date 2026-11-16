# Cơ bản về dịch vụ RAG bằng FastAPI

**Bài này minh họa:** Cách `create_app` tạo embedding cho cả 6 tài liệu FAQ đúng một lần lúc khởi tạo, phục vụ `/health`, trích nguồn trên `/ask` và từ chối câu hỏi thiếu ngữ cảnh mà không gọi `chat()`.

**Từng bước**
1. Các dòng 17–28 định nghĩa `SpyClient` bọc quanh `FakeLLM(embed_dim=256)` để ghi lại kích thước mỗi lô `embed` và đếm số lần gọi `chat`.
2. Các dòng 36–70 định nghĩa `create_app`, tạo `doc_vecs` một lần cho `DOCS` rồi gắn `/health` và `/ask` ngay trong closure.
3. Các dòng 74–87 gửi một request `/health` cùng ba câu hỏi `/ask`—hai câu có đáp án (`refunds`, `shipping`) và một câu ngoài tài liệu (`crypto`)—rồi in status, nguồn, câu trả lời và số lượt gọi.

**Lưu ý:** `index_embed` giữ nguyên là `1` qua mọi request, còn `chat` chỉ chạy `2` lần thay vì `3` vì câu hỏi crypto không có chunk nào đạt ngưỡng nên bị từ chối ngay.

**Tự thử:** Tăng `min_score` từ `0.2` lên `0.5` trong `create_app` và xem còn câu hỏi nào vượt được ngưỡng truy xuất.
