# So sánh kích thước chunk và độ gối

**Những gì ví dụ minh họa:** Chạy cùng ba câu hỏi chính sách qua bốn cấu hình cắt chunk `(size, overlap)` khác nhau và đếm số lần chunk hạng nhất chứa đúng cụm từ đáp án.

**Từng bước một**
1. Dòng 5–15 khai báo một tài liệu `DOC` gồm nhiều câu và ba cặp kiểm tra `(question, needle)`.
2. Dòng 18–28 định nghĩa `chunk_words(text, size, overlap)` với bước nhảy `step = size - overlap` và dừng ngay khi cửa sổ chạm cuối danh sách từ.
3. Dòng 31–44 duyệt qua `(5, 0)`, `(8, 0)`, `(8, 3)` và `(12, 3)`, embed từng bộ chunk và in ra số lượng chunk cùng số câu truy xuất trúng hạng nhất.

**Lưu ý:** Tăng `size` từ `5` lên `8` mà không có overlap chỉ bắt trúng `1/3` đáp án, thêm `overlap=3` nâng lên `2/3` và cấu hình `12/3` đạt `3/3`.

**Tự thử:** Thử thêm `(10, 4)` vào vòng lặp để xem tạo ra bao nhiêu chunk và đạt mấy câu trúng.
