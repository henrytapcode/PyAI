Bạn có một file CSV với hai cột `name` và `score`, và cần cùng dữ liệu đó ở dạng file JSON Lines, mỗi dòng một đối tượng. Hàm đã được viết sẵn, nhưng bốn từ bị thay bằng `___`. Hãy thay từng `___` để `csv_to_jsonl(csv_path, jsonl_path)` ghi mỗi dòng thành một đối tượng JSON (điểm là số) và trả về số dòng đã ghi. Phần 6 và 8 của bài học có đủ mọi mảnh bạn cần.

**Ví dụ**

| File CSV | File JSON Lines |
|---|---|
| `name,score` | |
| `Lan,9.5` | `{"name": "Lan", "score": 9.5}` |
| `Minh,7` | `{"name": "Minh", "score": 7.0}` |

Hàm trả về `2`.

**Quy tắc**
- Chỉ thay các chỗ `___`; phần code còn lại đã đúng.
- Giá trị CSV là chữ, nên điểm phải được đổi sang số.
- Giữ nguyên chữ không phải tiếng Anh (`ensure_ascii=False`).
