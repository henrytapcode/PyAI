# Làm phẳng các cuộc chat

**Ví dụ này cho thấy:** một comprehension có hai phần `for`, dùng để lấy mọi tin nhắn ra khỏi một list các cuộc chat.

**Từng bước**
1. Dòng 2–6 chứa ba cuộc chat. Mỗi chat là một list tin nhắn, và vài tin nhắn rỗng hoặc chỉ có dấu cách.
2. Dòng 8 có hai phần `for`. Hãy đọc theo thứ tự, như hai vòng lặp lồng nhau: với mỗi `chat` trong `chats`, rồi với mỗi `msg` trong `chat`. Kết quả là một list phẳng gồm 6 tin nhắn.
3. Dòng 11 thêm bộ lọc ở cuối. `msg.strip()` là chuỗi rỗng với tin nhắn trống, và chuỗi rỗng được coi là `False`, nên chúng bị bỏ. Các tin nhắn được giữ lại cũng đã được strip.
4. Dòng 14 tạo dict từ tin nhắn sang độ dài, nhưng chỉ cho tin nhắn có tối đa 10 ký tự.

**Để ý:** các phần `for` giữ **cùng thứ tự** với các vòng lặp bạn viết tay: vòng ngoài trước, vòng trong sau.

**Tự thử:** viết lại việc tương tự bằng hai vòng `for` lồng nhau với `append`, rồi kiểm tra bạn nhận được cùng một list.
