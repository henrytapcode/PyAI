# Script nạp giá đã được dọn gọn

**Ví dụ này cho thấy:** một script chuẩn bị dữ liệu nhỏ sau khi được dọn bằng ruff: mọi tên đều được dùng, `None` được kiểm tra bằng `is`, list mặc định là `None`, và `except` nêu đúng loại lỗi mong đợi.

**Từng bước**
1. Dòng 2–8 chứa các dòng dữ liệu thô, trong đó có dòng hỏng (`n/a`, thiếu tên).
2. Dòng 11–15 biến văn bản thành giá. `except ValueError` chỉ bắt lỗi "không phải số", nên một lỗi thật (như truyền `None`) vẫn lộ ra.
3. Dòng 18–24 tách một dòng thành tên và giá, và trả về `None` khi một trong hai phần không dùng được.
4. Dòng 27–37 lặp qua các dòng. List `skipped` mặc định là `None` và được tạo bên trong hàm (§6), nên hai lần gọi không bao giờ dùng chung nó.
5. Dòng 40–44 gọi hàm nạp rồi in các dòng tốt và các dòng bị bỏ qua.

**Để ý:** trước khi dọn, script này có một `import os` không ai dùng (`F401`), `if row == None` (`E711`), `except:` (`E722`) và `skipped=[]` (`B006`). Kết quả in ra trước và sau là như nhau. Việc dọn dẹp thay đổi độ an toàn của code, không thay đổi cái nó in ra với dữ liệu tốt.

**Tự thử:** thêm dòng `"Keyboard,45"` vào `RAW_LINES`. Kết quả in ra phải có thêm một dòng tốt.
