# Nhật ký chat

**Ví dụ này cho thấy:** một dataclass có method và một field kiểu list, dùng đúng cách các API chat mong đợi: một list các message, rồi chuyển thành list các dict.

**Từng bước**
1. Dòng 6–10 định nghĩa `Message` với hai field bắt buộc và một list `tags` bắt đầu rỗng cho mỗi message.
2. Dòng 12–13 thêm một method bình thường, `word_count`. Nó dùng `self` y như trong class thường.
3. Dòng 16–20 tạo ba message. Message thứ hai truyền `tags=["question"]`; các message còn lại dùng list rỗng mặc định.
4. Dòng 22–25 lại là mẫu bộ cộng dồn (accumulator): cộng số từ của mỗi message vào `total_words` rồi in message ra. Nội dung in ra đến từ `__repr__` mà `@dataclass` đã viết sẵn.
5. Dòng 28 so sánh một message trong list với một message mới tinh. Chúng là hai object khác nhau nhưng chứa cùng dữ liệu, nên `==` cho ra `True`.
6. Dòng 30–33 chuyển từng message thành dict bằng `asdict`, rồi in một cái dưới dạng JSON.

**Lưu ý:** `tags` của message đầu tiên là `[]` và không dùng chung với các message khác. Mỗi message nhận một list riêng từ `default_factory`.

**Tự thử:** thêm field `name: str = ""` sau `tags` rồi chạy lại. Mọi message in ra đều có field mới, và bạn không hề sửa `__repr__` nào.
