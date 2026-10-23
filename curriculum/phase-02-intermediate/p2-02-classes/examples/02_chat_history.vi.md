# Lịch sử chat

**Ví dụ này cho thấy:** object có thể chứa object khác. Một `ChatHistory` giữ một list các object `ChatMessage`, và mỗi tin nhắn tự biết cách đếm số từ của mình.

**Từng bước**
1. Dòng 2–11 định nghĩa `ChatMessage` với hai attribute, một method `word_count` và một `__repr__`.
2. Dòng 16 cho mỗi `ChatHistory` một list rỗng riêng. Vì list được tạo bên trong `__init__`, mỗi history có một list tách biệt.
3. Dòng 18–19 định nghĩa `add`. Nó tạo một `ChatMessage` rồi append vào `self.messages`.
4. Dòng 21–25 duyệt qua các tin nhắn và hỏi từng tin `word_count()` của nó. Đây là mẫu accumulator (biến cộng dồn), giờ nằm trong một method.
5. Dòng 27–32 giữ lại nội dung của tin nhắn mới nhất theo một role, hoặc `None` nếu không có.
6. Dòng 40 in list ra. Mỗi phần tử trong list được hiển thị bằng `__repr__` của nó.

**Để ý:** `history.messages` chỉ là một list bình thường. Class không giấu nó đi; nó chỉ giữ list đó cùng với các method làm việc trên nó.

**Tự thử:** thêm `history.add("assistant", "An object is one thing built from a class.")` trước các dòng print. `words:` sẽ tăng lên và `last_text("assistant")` sẽ trả về đoạn text mới.
