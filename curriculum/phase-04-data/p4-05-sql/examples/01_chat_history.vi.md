# Lưu lịch sử chat trong SQLite

**Ví dụ này cho thấy:** cách tạo bảng `messages`, thêm nhiều lượt chat bằng placeholder `?`, lấy hội thoại của một người dùng theo đúng thứ tự `id`, và đếm số tin nhắn theo từng `role`.

**Từng bước**
1. Dòng 4–12 mở database SQLite trong bộ nhớ và tạo bảng `messages` với cột `id` kiểu `INTEGER PRIMARY KEY`.
2. Dòng 14–25 thêm năm lượt chat bên trong `with conn:` bằng `executemany` và các placeholder `?`.
3. Dòng 27–37 lọc các tin nhắn của `"an"` sắp xếp theo `id ASC` rồi in từng dòng kèm id và vai trò.
4. Dòng 39–48 gom nhóm theo `role`, đếm từng nhóm, sắp theo `role ASC` rồi đóng kết nối.

**Để ý:** truyền `("an",)` có dấu phẩy ở cuối mới tạo ra tuple một phần tử; viết `("an")` thiếu dấu phẩy sẽ truyền chuỗi 2 ký tự và gây `ProgrammingError`.

**Tự thử:** đổi tham số ở `WHERE user = ?` thành `("binh",)` và xem hội thoại in ra có mấy tin nhắn.
