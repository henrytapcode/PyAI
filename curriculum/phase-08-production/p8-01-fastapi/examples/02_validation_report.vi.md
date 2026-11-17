# Báo cáo kiểm tra dữ liệu AskRequest

**Ví dụ này cho thấy:** Gửi một payload hợp lệ và bốn payload không hợp lệ khác nhau tới `POST /ask` để so sánh mã trạng thái HTTP và loại lỗi Pydantic trả về.

**Từng bước**
1. Dòng 10–12 định nghĩa `AskRequest` với `question` (`min_length=1`, `max_length=200`) và `top_k` (`default=3`, `ge=1`, `le=5`).
2. Dòng 15–17 đăng ký `POST /ask`; hàm chỉ chạy sau khi Pydantic kiểm tra xong JSON body.
3. Dòng 21–27 tạo năm payload thử nghiệm: một hợp lệ, một thiếu `question`, một chuỗi rỗng, một vượt ngưỡng (`top_k=9`) và một sai kiểu (`top_k="many"`).
4. Dòng 29–37 gửi từng payload qua `TestClient` và in bảng gọn gồm status code cùng `(loc, type)` của lỗi đầu tiên.

**Để ý:** Mỗi lỗi trả về một mã `type` cụ thể (`missing`, `string_too_short`, `less_than_equal`, `int_parsing`), còn hàm `ask()` chỉ thực sự chạy ở ca 1 khi dữ liệu đã sạch.

**Tự thử:** Thêm một payload có `"top_k": 0` và xem lỗi trả về là `greater_than_equal` vì ràng buộc `ge=1` không cho phép số 0.
