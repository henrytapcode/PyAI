# Danh sách lớp

**Ví dụ này cho thấy:** một list chứa các dictionary (mỗi học viên một dict), `.get()` với giá trị mặc định cho dữ liệu bị thiếu, và một tuple được tách ra.

**Từng bước**
1. Dòng 2–6 tạo một list gồm ba dict. Học viên thứ ba, Hoa, chưa có key `"score"`.
2. Dòng 8–9 chuẩn bị hai biến để nhớ học viên giỏi nhất cho đến lúc này.
3. Vòng lặp ở dòng 10–15 đi qua từng dict. Dòng 11 đọc điểm bằng `.get("score", 0)`, nên Hoa nhận `0` thay vì lỗi `KeyError`.
4. Dòng 12 in tên và điểm. Trong f-string ta dùng dấu nháy đơn (`'name'`) vì bản thân f-string đã dùng dấu nháy kép.
5. Dòng 13–15 là mẫu "giữ giá trị lớn nhất": nếu điểm này vượt điểm tốt nhất hiện tại thì ghi nhớ nó.
6. Dòng 17 in người thắng. Dòng 18 gói tên và điểm vào một tuple, dòng 19 tách nó lại thành hai biến.

**Để ý:** `student["name"]` an toàn ở đây vì học viên nào cũng có tên. Chỉ `"score"` có thể thiếu, nên chỉ nó dùng `.get()`.

**Tự thử:** cho Hoa `"score": 10` rồi chạy lại. Học viên giỏi nhất sẽ đổi thành Hoa.
