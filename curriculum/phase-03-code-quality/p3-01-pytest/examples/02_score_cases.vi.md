# Một bảng các case về điểm số

**Ví dụ này cho thấy:** ý tưởng đằng sau `parametrize`: một bảng gồm đầu vào và kết quả mong đợi, và một vòng lặp kiểm từng dòng. Điểm hợp lệ được so sánh như float với một sai số nhỏ, còn điểm không hợp lệ phải raise `ValueError`.

**Từng bước**
1. Dòng 2–6 định nghĩa `parse_score`. Nó raise `ValueError` trừ khi chuỗi có đúng một dấu `/`.
2. Dòng 9–16 định nghĩa `error_name`, trả về tên lỗi mà một lời gọi raise, hoặc `"no error"`.
3. Dòng 19–20 chứa các case: `VALID` là các cặp chuỗi và số mong đợi, `INVALID` là các chuỗi phải bị từ chối.
4. Dòng 23–29 kiểm từng case hợp lệ bằng `abs(result - expected) < 1e-3` thay vì `==`.
5. Dòng 31–37 kiểm mỗi chuỗi không hợp lệ có raise `ValueError` không.
6. Dòng 39 in ra có bao nhiêu case ổn.

**Để ý:** dòng áp chót của kết quả là `FAIL 8/0`. Chia cho 0 raise `ZeroDivisionError`, không phải `ValueError`. Bảng case đã tìm ra một lỗ hổng mà tác giả không nghĩ tới.

**Tự thử:** sửa `parse_score` để `"8/0"` raise `ValueError` (kiểm số thứ hai trước khi chia), rồi chạy lại. Cả bảng phải xanh.
