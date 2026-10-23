# Request chat có type hint

**Ví dụ này cho thấy:** một dataclass có các field là type hint, gồm cả system prompt tùy chọn `system`, và một hàm biến nó thành list các message.

**Từng bước**
1. Dòng 5–10 định nghĩa `ChatRequest`. Mỗi field có một hint. `system: str | None = None` nghĩa là field này tùy chọn và mặc định là `None`.
2. Dòng 13–18 nhận một `ChatRequest` và trả về `list[dict[str, str]]`.
3. Dòng 15 dùng `is not None` (ngược với `is None`) để message system chỉ được thêm khi có system prompt.
4. Dòng 21–22 tạo một request không có system prompt và một request có.
5. Dòng 23–25 in request và hai list message.

**Lưu ý:** request thường hoàn toàn không có message `"system"`, vì `system` vẫn là `None`. Hint và giá trị mặc định phối hợp với nhau ở đây.

**Thử tự làm:** đổi đối số cuối của `careful` từ `0.2` thành `"hot"`. Python vẫn chạy, vì hint trong dataclass không bị kiểm tra.
