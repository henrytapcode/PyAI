# Lọc trước khi lấy top-k (Pre-filter và Post-filter)

**Những gì ví dụ minh họa:** Vì sao áp dụng bộ lọc metadata *trước* khi xếp hạng top-k luôn trả đủ `k` kết quả phù hợp, còn lọc *sau* top-k có thể rơi xuống 0 kết quả.

**Từng bước một**
1. Dòng 5–21 embed sáu bản ghi song ngữ cùng câu hỏi `"money back for laptop"`, với `k = 2` và `where = {"lang": "vi"}`.
2. Dòng 24–30 chạy **post-filter**: lấy top-2 toàn cục (`d2` và `d1`, đều là tiếng Anh) rồi mới lọc `lang == "vi"`, nên kết quả còn `0`.
3. Dòng 33–39 chạy **pre-filter**: cắt `matrix[kept]` chỉ giữ ba dòng `"vi"` trước rồi mới lấy top-2, trả về đủ `[('d4', 0.516), ('d5', 0.236)]`.

**Lưu ý:** Cả hai cách dùng chung một bảng điểm; chỉ cần đảo thứ tự lọc và cắt `[:k]` là kết quả đổi từ `0` thành đủ `2` mục.

**Tự thử:** Tăng `k` lên `4` ở đoạn post-filter và xem có bao nhiêu kết quả `"vi"` lọt qua (`1` thay vì `2`).
