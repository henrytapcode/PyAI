Một pipeline có nhiều bước, và bạn muốn có một log cho biết mỗi bước bắt đầu và kết thúc lúc nào, kể cả khi bước đó bị lỗi. Context manager `logged_step(log, name)` đã được viết sẵn, nhưng ba chỗ đã bị thay bằng `___`. Hãy thay mỗi `___` để manager thêm `"start <name>"` vào list `log` khi khối bắt đầu, thêm `"end <name>"` khi khối kết thúc, và đưa tên của bước cho `as`. Rồi bấm **Kiểm tra**.

**Ví dụ**

| code | `log` sau đó |
|---|---|
| `with logged_step(log, "embed"): ...` | `["start embed", "end embed"]` |
| `with logged_step(log, "embed") as step: ...` | `step` là `"embed"` |

**Quy tắc**
- `"start <name>"` được thêm **trước** khi phần thân của `with` chạy.
- `"end <name>"` được thêm khi phần thân kết thúc, kể cả khi phần thân raise lỗi.
- Lỗi được raise ra trong phần thân không bị giấu: nó vẫn đến được code bao quanh `with`.
- Giữ nguyên `try` và `finally`; bạn chỉ điền vào các chỗ trống.
