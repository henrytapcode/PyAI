# Điều phối tool an toàn trước các lỗi thường gặp

**Điểm nổi bật:** Hàm `dispatch()` xử lý năm `ToolCall` khác nhau—hợp lệ kèm tham số tùy chọn rỗng, tool lạ, thiếu tham số bắt buộc, sai kiểu dữ liệu và hàm ném `ValueError`—mà không làm sập chương trình.

**Từng bước**
1. Dòng 9–22 định nghĩa `get_weather()` (ném `ValueError` khi không thấy thành phố), `add_tax()` (báo `TypeError` nếu `price` không phải số), cùng `REGISTRY` và `REQUIRED`.
2. Dòng 25–38 cài đặt `dispatch()`: từ chối tên tool lạ, kiểm tra khóa bắt buộc khác `("", None)`, lọc bỏ giá trị rỗng giả của tham số tùy chọn, chạy `registry[call.name](**clean)` trong `try/except` và đổi `dict` bằng `json.dumps()`.
3. Dòng 41–50 dựng năm `ToolCall` gồm một ca hợp lệ và bốn ca lỗi, rồi in chuỗi kết quả của từng ca.

**Lưu ý:** Thay vì văng lỗi dừng chương trình ở `call_2` đến `call_5`, `dispatch()` trả về chuỗi `"error: ..."` để gửi lại ngay cho LLM dưới dạng message `tool`.

**Tự thử:** Thêm một `ToolCall` hợp lệ cho `add_tax` với `{"price": 20.0}` vào `test_calls` và kiểm tra `dispatch()` trả về `"22.0"`.
