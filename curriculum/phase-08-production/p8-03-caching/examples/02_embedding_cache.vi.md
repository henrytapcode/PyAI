# Cache embedding theo lô khi lập chỉ mục lại tài liệu

**Ví dụ này cho thấy:** Lập chỉ mục lại 6 tài liệu sau khi sửa 2 tài liệu sao cho `client.embed()` chỉ phải chạy cho đúng 2 đoạn mới sửa mà 6 vector trả về vẫn giữ nguyên thứ tự ban đầu.

**Từng bước**
1. Dòng 6–26 viết hàm `embed_batch_cached(client, model, texts, cache)`: gom các văn bản chưa có trong cache theo key `(model, text)`, gọi `client.embed(missing)` một lần cho cả batch thiếu, rồi ghép danh sách `ordered` theo đúng thứ tự `texts`.
2. Dòng 29–44 lập chỉ mục lần 1 cho 6 tài liệu (`docs_v1`), gửi đủ `6/6` văn bản tới `embed()`.
3. Dòng 46–55 sửa tài liệu ở vị trí `1` và `4` trong `docs_v2`, chạy lại (`2/6` văn bản được gửi) và kiểm tra `match: True` so với gọi thẳng `client.embed(docs_v2)`.

**Để ý:** Dùng key `(model, text)` giúp tái sử dụng vector của các tài liệu không đổi, đồng thời đảm bảo khi đổi sang model khác (như `"embed-v2"`) sẽ không bao giờ dùng nhầm vector của model cũ.

**Tự thử:** Đổi `model` từ `"embed-v1"` sang `"embed-v2"` trước lần chạy thứ hai rồi kiểm tra xem số văn bản phải gửi có tăng lại thành `6/6` không.
