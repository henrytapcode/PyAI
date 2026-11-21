Hãy cài đặt hai hàm hỗ trợ chạy script bằng Python thuần:

1. `find_python_files(entries: list[str], folder: str = "") -> list[str]`:
   - Cắt khoảng trắng và dấu `"/"` ở đầu mỗi phần tử trong `entries`, chỉ giữ các phần tử kết thúc bằng `".py"`.
   - Chuẩn hóa `folder` bằng cách cắt khoảng trắng và dấu `"/"` ở đầu/cuối.
   - Nếu `folder` khác rỗng, chỉ giữ các file `.py` nằm bên trong thư mục đó theo ranh giới `"/"` (ví dụ `folder="src"` khớp `"src/app.py"` và `"src/utils/io.py"`, nhưng **không bao giờ** khớp `"src_old/a.py"`).
   - Trả về danh sách đường dẫn đã chuẩn hóa, sắp xếp tăng dần.

2. `build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]`:
   - Cắt khoảng trắng ở `script`; ném `ValueError` nếu không kết thúc bằng `".py"`.
   - Trả về `["uv", "run", "python", script, *args]` khi `use_uv=True`, hoặc `["python", script, *args]` khi `use_uv=False` (không thêm gì nếu `args` là `None` hoặc rỗng).

### Ví dụ
```python
find_python_files(["src/b.py", "src_old/a.py", "src/a.py", "README.md"], folder="src/")
# ["src/a.py", "src/b.py"]

build_run_cmd("src/app.py", ["--port", "8000"], use_uv=True)
# ["uv", "run", "python", "src/app.py", "--port", "8000"]
```
