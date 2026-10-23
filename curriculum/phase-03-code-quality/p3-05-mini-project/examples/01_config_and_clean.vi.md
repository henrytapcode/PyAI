# Một văn bản, hai config

**Ví dụ này cho thấy:** cùng một hàm `clean_text` cho kết quả khác nhau khi bạn đưa cho nó một `CleanConfig` khác. Các bước làm sạch không đổi; chỉ có thiết lập thay đổi.

**Từng bước**
1. Dòng 5–9 định nghĩa config frozen. Mọi tùy chọn đều có giá trị mặc định, nên `CleanConfig()` là thiết lập bình thường.
2. Dòng 12–18 là hai hàm thuần nhỏ: một hàm sửa khoảng trắng, một hàm bỏ các từ bắt đầu bằng `http://` hoặc `https://`.
3. Dòng 21–33 là `clean_text`. Nó kiểm tra kiểu, chọn config mặc định khi không được truyền vào, và chạy các bước theo thứ tự cố định: link, khoảng trắng, chữ hoa/thường, độ dài.
4. Dòng 41–42 tạo hai config: config bình thường, và một config giữ chữ hoa rồi cắt còn 12 ký tự.
5. Dòng 44–45 in cả hai kết quả cho mỗi review, để bạn so sánh cạnh nhau.

**Lưu ý:** ở cột thứ hai, `Great PRODUC` bị cắt sau 12 ký tự và `Too SLOW to` không có khoảng trắng ở cuối, vì `rstrip()` bỏ khoảng trắng do việc cắt để lại.

**Thử tự làm:** tạo config thứ ba, `CleanConfig(drop_urls=False)`, và in review đầu tiên với nó. Đường link sẽ còn nguyên trong văn bản.
