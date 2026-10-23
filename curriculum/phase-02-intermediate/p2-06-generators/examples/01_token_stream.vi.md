# Luồng token

**Ví dụ này cho thấy:** một generator đưa ra câu trả lời từng token một, giống chatbot gõ dần câu trả lời.

**Từng bước**
1. Dòng 2–4 định nghĩa `stream_reply`. Nó cắt văn bản thành các từ và `yield` từng từ một. Khi bạn gọi hàm, chưa có gì chạy cả.
2. Dòng 8 tạo generator object. Dòng 10 xin token đầu tiên bằng `next`.
3. Dòng 13–14 dùng vòng `for` trên cùng generator đó. Nó tiếp tục từ token thứ hai, vì token đầu đã được lấy rồi.
4. Dòng 16 gọi lại `stream_reply` để có một generator **mới** và nối tất cả token của nó lại bằng `"".join(...)`.

**Lưu ý:** vòng lặp ở dòng 13–14 không in lại `Generators`. Generator nhớ vị trí của nó nên chỉ đưa ra phần còn lại.

**Thử tự làm:** thêm vòng `for token in stream:` thứ hai sau dòng 14 rồi chạy. Nó không in gì cả, vì generator đã cạn.
