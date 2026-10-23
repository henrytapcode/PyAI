Một giáo viên xuất điểm thi ra dạng văn bản, và vài dòng bị hỏng. Hãy viết `load_scores(raw_scores)`. Hàm nhận một list các chuỗi, đổi từng chuỗi thành `int`, và trả về list các số. Hàm cũng **ghi log những gì đã xảy ra**, để người đọc log thấy được dòng nào bị bỏ qua. Viết code bên trong hàm và `return` kết quả.

**Ví dụ**

| lời gọi | trả về | các log record |
|---|---|---|
| `load_scores(["10", "7"])` | `[10, 7]` | `INFO` `loaded 2 of 2 scores` |
| `load_scores(["10", "abc", "7"])` | `[10, 7]` | `WARNING` `skipping bad score: abc`, rồi `INFO` `loaded 2 of 3 scores` |
| `load_scores([])` | `[]` | `INFO` `loaded 0 of 0 scores` |

**Quy tắc**
- Một chuỗi mà `int()` không đổi được (nó raise `ValueError`) thì bị bỏ qua. Ghi **một** record ở mức `WARNING` cho nó, với đúng thông điệp `skipping bad score: <text>`, trong đó `<text>` là chuỗi gốc.
- Sau vòng lặp, ghi **một** record ở mức `INFO`, với đúng thông điệp `loaded <n> of <total> scores`, trong đó `<n>` là số điểm hợp lệ và `<total>` là độ dài của `raw_scores`.
- Không ghi log nào khác, và không dùng `print`.
- Các điểm hợp lệ giữ nguyên thứ tự ban đầu.
- Dùng `logger` ở cấp module đã có sẵn trong code khởi đầu.
