# Lỗi xảy ra ở đâu?

**Ví dụ này cho thấy:** một chương trình bắt lỗi và báo cáo đúng những điều bạn đọc từ traceback: loại lỗi, thông báo, và chuỗi lời gọi dẫn tới lỗi.

**Từng bước**
1. Dòng 5–6 định nghĩa `parse_score`, hàm gọi `int(text)` và có thể ném `ValueError`.
2. Dòng 9–13 định nghĩa `load_scores`, hàm gọi `parse_score` cho từng dòng trong vòng lặp `for`.
3. Bên trong `main`, dòng 18 gọi `load_scores` với giá trị ở giữa là `"abc"`, không thể thành số.
4. Dòng 20 yêu cầu module `traceback` cho các frame của lỗi. `err.__traceback__` giữ chuỗi các lời gọi, và `traceback.extract_tb` biến nó thành list các frame. Mỗi frame có một `name`.
5. Output hiện loại lỗi và thông báo trước, rồi đường đi `main -> load_scores -> parse_score`. Đây là cùng câu chuyện với traceback in ra, nhưng đọc từ trên xuống.

**Lưu ý:** tên cuối cùng trong đường đi, `parse_score`, là nơi lỗi được ném ra. Câu hỏi thật sự là vì sao `load_scores` lại gửi cho nó `"abc"`.

**Thử tự làm:** đổi `"abc"` thành `"5"`. Nhánh `except` không chạy, nên không có gì được in ra.
