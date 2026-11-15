Cài đặt hàm `score_grounded(answer, expected_facts, context)` trong `starter.py`. Đây là bản mở rộng của hàm `score_answer` ở §4: ngoài việc chấm đủ fact và phát hiện từ không có trong ngữ cảnh, câu trả lời bám nguồn còn phải trích dẫn đúng các nguồn có thật trong `context`.

Viết code bên trong hàm (có thể thêm hàm phụ) và `return` một dictionary:

```python
{
    "facts": float,
    "faithful": bool,
    "unsupported": list[str],
    "citations": list[int],
    "bad_citations": list[int],
}
```

## Bảng ví dụ

Giả sử `context` gồm hai dòng nguồn:

```text
[1] Refunds are issued within 30 days of purchase.
[2] Standard shipping arrives within 5 business days.
```

| answer | expected_facts | facts | faithful | unsupported | citations | bad_citations |
|---|---|---|---|---|---|---|
| `"Refunds are issued within 30 days. [1]"` | `["30 days"]` | `1.0` | `True` | `[]` | `[1]` | `[]` |
| `"Refunds are issued within 30 days."` | `["30 days"]` | `1.0` | `False` | `[]` | `[]` | `[]` |
| `"Refunds are issued within 30 days. [3]"` | `["30 days"]` | `1.0` | `False` | `[]` | `[3]` | `[3]` |
| `"Shipping takes 5 days [2], refunds 30 days [1] [2]."` | `["5 days", "30 days"]` | `1.0` | `True` | `[]` | `[2, 1]` | `[]` |
| `"I don't know based on the provided context."` | `[]` | `1.0` | `True` | `[]` | `[]` | `[]` |

## Quy tắc

- **`facts` (`float`):**
  - Nếu `expected_facts` rỗng, trả về `1.0` khi `"i don't know"` có trong `answer.lower()`, ngược lại trả `0.0`.
  - Ngược lại, trả về tỉ lệ các phần tử trong `expected_facts` thỏa `fact.lower() in answer.lower()`.
- **`citations` (`list[int]`):**
  - Trích mọi số nguyên `n` trong các thẻ `[n]` (`\[(\d+)\]`) của `answer`, giữ đúng thứ tự xuất hiện đầu tiên và không trùng lặp (ví dụ `"[2] ... [1] ... [2]"` cho ra `[2, 1]`).
  - Vẫn tính `citations` bình thường ngay cả khi `answer` chứa `"i don't know"`.
- **`bad_citations` (`list[int]`):**
  - `context` gồm các dòng dạng `"[n] text"` nối bằng `\n`. Lấy tập các số nguồn hợp lệ `[n]` nằm ở đầu dòng trong `context` (cho phép khoảng trắng đầu dòng).
  - `bad_citations` là các số trong `citations` (theo đúng thứ tự) không có dòng `[n] ...` tương ứng trong `context`.
- **Quy tắc tách từ nội dung và `unsupported` (`list[str]`):**
  1. Đổi toàn bộ văn bản sang chữ thường.
  2. Xóa các trích dẫn dạng `\[\d+\]` (như `[1]` hoặc `[12]`).
  3. Tách các từ chữ và số bằng regex `[a-z0-9]+`.
  4. Chỉ giữ các từ có `len(word) >= 4`.
  - Ví dụ: `"[1] Refunds take 30 days for all items."` cho ra `["refunds", "take", "days", "items"]` (`[1]`, `30`, `for`, `all` bị bỏ qua).
  - Nếu `"i don't know"` có trong `answer.lower()`, `unsupported` bằng `[]`.
  - Ngược lại, `unsupported` gom mọi từ nội dung của `answer` không nằm trong tập từ nội dung của `context`, giữ đúng thứ tự xuất hiện đầu tiên và không trùng lặp.
- **`faithful` (`bool`):**
  - Bằng `True` nếu `"i don't know"` có trong `answer.lower()`, **hoặc** khi `unsupported` rỗng **và** `citations` khác rỗng **và** `bad_citations` rỗng.
  - Ngược lại bằng `False` (ví dụ: không có trích dẫn, hoặc trích `[3]` khi `context` chỉ có `[1]`, `[2]`).
- Không được sửa đổi list `expected_facts` truyền vào.
