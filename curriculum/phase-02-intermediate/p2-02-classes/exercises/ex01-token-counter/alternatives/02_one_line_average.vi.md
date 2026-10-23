# Trung bình trong một dòng

Cách này viết đầy đủ `self.total = self.total + n` thay cho `+=`, và nén `average` vào một dòng bằng `A if điều_kiện else B`. Đây là **conditional expression** (biểu thức điều kiện) trong bài Comprehension (§4), chọn một trong hai giá trị. `self.calls` được coi là đúng khi khác 0. Cách này ngắn hơn, nhưng `if` thường với `return` sớm trong lời giải chính dễ đọc hơn cho người mới.
