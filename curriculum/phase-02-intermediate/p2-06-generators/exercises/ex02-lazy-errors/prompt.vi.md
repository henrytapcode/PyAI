File log có thể có hàng triệu dòng, nên bạn đọc nó theo kiểu lười. Hai hàm đã được viết sẵn, nhưng ba từ bị thay bằng `___`. Hãy thay từng `___` để `error_lines(lines)` yield mọi dòng có chứa `ERROR` (đã bỏ dấu cách và ký tự xuống dòng ở hai đầu), và `count_errors(lines)` trả về số dòng như vậy. Sau đó bấm **Kiểm tra**.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `list(error_lines(["ok\n", "ERROR disk full\n"]))` | `["ERROR disk full"]` |
| `count_errors(["ERROR a\n", "ok\n", "ERROR b\n"])` | `2` |

**Quy tắc**
- `lines` có thể là iterable bất kỳ chứa các chuỗi: list, file đang mở, hoặc generator.
- Khớp đúng chữ `ERROR` (chữ hoa). Dòng chứa `error` viết thường thì không tính.
- `error_lines` là generator: nó chỉ đọc đúng số dòng cần thiết cho phần tử mà bạn xin.
- Giữ nguyên thứ tự các dòng.
