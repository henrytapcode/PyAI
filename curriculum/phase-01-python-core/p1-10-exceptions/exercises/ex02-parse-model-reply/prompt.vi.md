Một model phân loại lẽ ra phải trả lời bằng JSON như `{"label": "spam", "score": 0.9}`, nhưng reply thật đôi khi bị hỏng. Hãy viết `parse_reply(text)` sao cho không bao giờ sập: nó trả về `label` và `score` đã đọc được, hoặc một kết quả "unknown" an toàn. Sau đó viết `count_unknown(replies)`. Viết code bên trong hàm và `return` kết quả.

**Ví dụ**

| đầu vào | kết quả |
|---|---|
| `'{"label": "spam", "score": 0.9}'` | `{"label": "spam", "score": 0.9}` |
| `"Sure! Here is the JSON"` | `{"label": "unknown", "score": 0.0}` |
| `'{"label": "ham"}'` | `{"label": "unknown", "score": 0.0}` |
| `'{"label": "ham", "score": 1.5}'` | `{"label": "unknown", "score": 0.0}` |

**Quy tắc**
- Dùng `json.loads` (module `json` đã được import sẵn trong starter).
- Kết quả dự phòng dùng cho: JSON không hợp lệ, thiếu `"label"` hoặc `"score"`, JSON không phải dict (như một list), score không phải số, và score nhỏ hơn `0` hoặc lớn hơn `1`.
- `0` và `1` là score hợp lệ.
- `count_unknown(replies)` trả về số reply trong list cho ra kết quả unknown.
- Không dùng `except:` trần. Hãy nêu tên các loại lỗi.
