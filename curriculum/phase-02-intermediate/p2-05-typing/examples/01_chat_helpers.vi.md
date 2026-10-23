# Hàm hỗ trợ chat có type hint

**Ví dụ này cho thấy:** bốn hàm nhỏ có hint mô tả một cuộc hội thoại: nhận vào list các dict, trả ra một số, một `str | None` hoặc một tuple.

**Từng bước**
1. Dòng 2–3 tạo một message. Hint trả về `dict[str, str]` cho biết cả key lẫn value đều là văn bản.
2. Dòng 6–10 nhận `list[dict[str, str]]` và trả về `int`: tổng số từ, dùng biến tích lũy (accumulator).
3. Dòng 13–18 trả về `str | None`. Nếu không message nào có role đó thì `found` vẫn là `None`, nên hint phải cho phép `None`.
4. Dòng 21–22 trả về `tuple[int, int]`: hai số ở vị trí cố định.
5. Dòng 25–29 tạo cuộc hội thoại. Dòng 31–32 cho thấy cả hai kết quả của `last_from`.
6. Dòng 33 tách tuple vào `count` và `words`.

**Lưu ý:** hint cho bạn biết mỗi hàm trả về gì trước khi đọc phần thân. Dòng 32 in `None` vì không ai có role `"system"`.

**Thử tự làm:** thêm `make_message("system", "Be brief.")` vào `chat`. Dòng 32 giờ sẽ in `Be brief.` thay vì `None`.
