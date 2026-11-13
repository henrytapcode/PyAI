# Log phiên trò chuyện chatbot

**Ví dụ này cho thấy:** cách tạo DataFrame từ dict chứa các list, lọc hàng theo đánh giá và sắp xếp theo nhiều cột.

**Từng bước**
1. Dòng 4–8 tạo DataFrame `logs` với năm phiên chatbot cùng điểm đánh giá của người dùng.
2. Dòng 10 in tổng số phiên bằng `len(logs)`.
3. Dòng 11–13 lọc các phiên có `rating <= 2`, sắp xếp theo điểm đánh giá tăng dần rồi số tin nhắn giảm dần, và đánh lại số hàng bằng `.reset_index(drop=True)`.
4. Dòng 16 in ra bảng đã lọc và sắp xếp.

**Để ý:** `ascending=[True, False]` sắp `rating` từ thấp đến cao và khi bằng điểm thì xếp `messages` từ cao xuống thấp, còn `.reset_index(drop=True)` đưa nhãn hàng về lại `0, 1, 2`.

**Tự thử:** đổi `rating <= 2` ở dòng 11 thành `rating <= 4` rồi xem những phiên nào được giữ lại.
