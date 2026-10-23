Bạn có một file text, mỗi dòng là một prompt, nhưng file hơi lộn xộn: vài dòng thừa khoảng trắng, vài dòng trống. Hãy viết `read_clean_lines(path)` để mở file, `strip` từng dòng, bỏ qua dòng trống và trả về phần còn lại dưới dạng list các chuỗi. Viết code bên trong hàm và `return` kết quả. Phần 3 của bài học cho bạn cách lặp qua một file.

**Ví dụ**

| Nội dung file | Trả về |
|---|---|
| `"  hello \n\nworld\n"` | `["hello", "world"]` |
| `"Xin chào\n"` | `["Xin chào"]` |
| `""` (file rỗng) | `[]` |

**Quy tắc**
- Mở file với `encoding="utf-8"`.
- Không sửa file; chỉ đọc.
- Trả về list các chuỗi không có `\n`.
