# Đếm token, padding theo batch và cắt độ dài

**Điều cần thấy:** Chỉ dùng `AutoTokenizer` để đếm số mảnh token, xem shape của batch sau khi padding và quan sát `max_length` cắt bớt câu dài.

**Từng bước**
1. Dòng 4–7 nạp tokenizer đã ghim từ cache với `local_files_only=True` (không cần nạp trọng số model).
2. Dòng 9–18 gọi `tokenizer.tokenize(text)` trên bốn câu để đếm số mảnh token không tính `[CLS]` và `[SEP]`, rồi in độ dài lớn nhất (`10`).
3. Dòng 20–21 tokenize cả bốn câu thành một batch với `padding=True, truncation=True, return_tensors="pt"` và in shape ma trận `(4, 12)` (`10` token của câu dài nhất cộng thêm `[CLS]` và `[SEP]`).
4. Dòng 23–26 tokenize một câu dài với `truncation=True, max_length=8` rồi in 8 token còn lại sau khi cắt.

**Lưu ý:** Câu dài nhất có `10` token thường nhưng chiều rộng của batch sau padding là `12`, vì `tokenizer(...)` luôn gắn thêm `[CLS]` ở đầu và `[SEP]` ở cuối.

**Thử tự sửa:** Đổi `max_length=8` thành `max_length=10` rồi xem `'##point'` và `'timed'` xuất hiện trở lại trước `[SEP]`.
