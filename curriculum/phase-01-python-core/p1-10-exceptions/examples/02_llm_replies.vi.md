# Đọc reply của model một cách an toàn

**Ví dụ này cho thấy:** cách đọc JSON do một language model trả về, khi thì hợp lệ, khi thì là văn bản lan man, mà không làm sập pipeline.

**Từng bước**
1. Dòng 7 gọi `json.loads(text)`, biến văn bản JSON thành dict. Nó gây `json.JSONDecodeError` khi văn bản không phải JSON hợp lệ.
2. Dòng 8 đọc hai trường cần dùng. Thiếu trường sẽ gây `KeyError`. Nếu JSON là thứ khác, ví dụ một list, thì `data["label"]` gây `TypeError`.
3. Dòng 9–10 xử lý JSON hỏng. `as err` cho ta đối tượng lỗi, và `err.msg` là thông báo ngắn của nó (`Expecting value`).
4. Dòng 11–12 xử lý thiếu trường hoặc JSON sai dạng bằng một tuple hai loại lỗi.
5. Dòng 13 là **fallback** (phương án dự phòng): sau mọi lỗi đã xử lý, ta trả về kết quả "unknown" an toàn, nên bên gọi luôn nhận được dict có cùng các key.
6. Vòng lặp ở cuối thử cả bốn trường hợp: JSON tốt, văn bản lan man, thiếu trường, rồi lại JSON tốt.

**Để ý:** thứ tự của hai khối `except` này không quan trọng, vì không loại nào là một dạng của loại kia. Thứ tự chỉ quan trọng khi một loại là một dạng của loại khác (xem cây ở mục 3 của bài): Python dùng khối đầu tiên khớp.

**Tự thử:** thêm reply `'["spam", 0.9]'` vào `replies`. Bạn đoán sẽ thấy thông báo nào? (List không đọc được bằng `["label"]`, nên bạn thấy `JSON is missing a field`.)
