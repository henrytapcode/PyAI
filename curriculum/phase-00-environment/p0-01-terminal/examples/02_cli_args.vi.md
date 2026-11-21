# Tham số dòng lệnh và mã thoát

**Ví dụ này minh họa:** cách một script nhận danh sách token kiểu `argv` và trả về mã thoát số nguyên (`0` khi thành công, khác `0` khi có lỗi).

**Từng bước một**
1. `run_cli` kiểm tra xem có token nào không; nếu rỗng thì in lỗi và trả về `1`.
2. `tokens[0]` là tên script và `tokens[1:]` là các tham số còn lại.
3. Nếu tên script không kết thúc bằng `.py`, hàm trả về mã thoát `2`.
4. Đầu vào hợp lệ sẽ in tên script cùng tham số và trả về `0`.

**Tự thử:** thêm `["eval.py", "--fast"]` vào danh sách mẫu rồi xem mã thoát của nó.
