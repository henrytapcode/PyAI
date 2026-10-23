Các dịch vụ embedding chỉ nhận một số lượng văn bản giới hạn mỗi lần gọi, nên bạn gửi tài liệu theo từng lô nhỏ. Hãy viết hàm generator `batched(items, n)`. Nó duyệt qua `items` và yield các list có tối đa `n` phần tử, mỗi lần một list. Hãy viết code bên trong hàm và `yield` từng lô.

**Ví dụ**

| lời gọi | những gì nhận được lần lượt |
|---|---|
| `batched([1, 2, 3, 4, 5], 2)` | `[1, 2]`, rồi `[3, 4]`, rồi `[5]` |
| `batched("abcd", 2)` | `["a", "b"]`, rồi `["c", "d"]` |
| `batched([], 3)` | không có gì |

**Quy tắc**
- `items` có thể là iterable bất kỳ: list, tuple, chuỗi, `range`, hoặc một generator khác. `n` ít nhất là 1.
- Mỗi lô là một list, theo đúng thứ tự ban đầu. Lô cuối có thể ngắn hơn `n`, nhưng không bao giờ rỗng.
- Mỗi lô phải là một list mới riêng biệt. Đừng dùng lại rồi làm rỗng cùng một list.
- Hãy lười: sau khi lô đầu tiên được xin, chỉ đọc đúng số phần tử mà lô đó cần.
- Không thay đổi dữ liệu đầu vào.
