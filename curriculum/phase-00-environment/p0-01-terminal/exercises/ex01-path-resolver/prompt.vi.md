Hãy cài đặt hai hàm hỗ trợ terminal bằng Python thuần:

1. `resolve_path(cwd: str, target: str) -> str`:
   - Phân giải `target` dựa trên `cwd` theo chuẩn đường dẫn POSIX dùng dấu `/`.
   - Nếu `target` bắt đầu bằng `"/"`, đó là đường dẫn **tuyệt đối** (bỏ qua `cwd`).
   - Ngược lại, đó là đường dẫn **tương đối** tính từ `cwd`.
   - Gộp các dấu `/` trùng nhau (`//`), bỏ qua `.`, và lùi một thư mục khi gặp `..` (dừng lại ở `"/"` nếu đã ở thư mục gốc).
   - Luôn trả về đường dẫn chuẩn hóa bắt đầu bằng `"/"` và không có `/` ở cuối (ngoại trừ chính `"/"`).

2. `split_command(line: str) -> tuple[str, list[str]]`:
   - Cắt khoảng trắng đầu/cuối và tách `line` theo khoảng trắng.
   - Trả về `(cmd, args)` với `cmd` là token đầu tiên và `args` là danh sách các token còn lại.
   - Ném `ValueError` nếu `line` rỗng hoặc chỉ chứa khoảng trắng.

### Ví dụ
```python
resolve_path("/home/alex/app", "../data/./notes.txt")  # "/home/alex/data/notes.txt"
resolve_path("/home/alex", "../../../etc")             # "/etc"
resolve_path("/home/alex", "/var/log//app")            # "/var/log/app"
split_command("  python  main.py --fast ")             # ("python", ["main.py", "--fast"])
```
