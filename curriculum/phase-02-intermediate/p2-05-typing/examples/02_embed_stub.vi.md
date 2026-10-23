# Hàm embedding giả có type hint

**Ví dụ này cho thấy:** một hàm `embed` giả có cùng chữ ký với hàm thật, và chuyện gì xảy ra khi bạn vi phạm hint của nó.

**Từng bước**
1. Dòng 2–6 biến mỗi văn bản thành vector hai số thực (độ dài và số chữ `"a"`; `text.count("a")` đếm xem `"a"` xuất hiện bao nhiêu lần). Hint: nhận `list[str]`, trả về `list[list[float]]`.
2. Dòng 9–13 nhận hai vector và trả về tích vô hướng (dot product: nhân các số ở cùng vị trí rồi cộng lại) dạng `float`.
3. Dòng 16–18 embed hai từ rồi in các vector và tích vô hướng của chúng.
4. Dòng 21 truyền một `str` đơn lẻ thay vì một list. Điều này vi phạm hint.
5. Dòng 22 in các hint mà Python đã lưu trên hàm.

**Lưu ý:** dòng 21 chạy mà không có lỗi nào. Duyệt qua `"cat"` đi qua `c`, `a`, `t`, nên bạn nhận ba vector thay vì một. Type checker sẽ bắt lời gọi này trước khi bạn chạy.

**Thử tự làm:** gọi `embed(["cat"])` (list có một từ) và so sánh kết quả với dòng 21.
