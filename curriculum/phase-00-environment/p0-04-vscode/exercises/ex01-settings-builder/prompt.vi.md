Viết hai hàm trong `starter.py` để tạo và kiểm tra cấu hình `.vscode/settings.json`:

1. `build_vscode_settings(venv_path: str, line_length: int = 100, format_on_save: bool = True) -> dict`
   - Cắt khoảng trắng đầu/cuối của `venv_path`.
   - Ném `ValueError` nếu `venv_path.strip()` rỗng hoặc `line_length` nằm ngoài đoạn `[40, 200]` (`not (40 <= line_length <= 200)`).
   - Trả về dictionary với đúng các key và giá trị sau:
     - `"python.defaultInterpreterPath"`: `venv_path` đã cắt khoảng trắng
     - `"editor.formatOnSave"`: `bool(format_on_save)`
     - `"ruff.lineLength"`: `line_length`
     - `"[python]"`: `{"editor.defaultFormatter": "charliermarsh.ruff"}`

2. `validate_settings_json(raw_json: str) -> tuple[bool, list[str]]`
   - Phân tích `raw_json` bằng `json.loads()`.
   - Nếu `raw_json` không phải JSON hợp lệ hoặc giá trị top-level không phải `dict`, trả về `(False, ["invalid_json"])`.
   - Ngược lại, kiểm tra các key bắt buộc theo đúng thứ tự: `"python.defaultInterpreterPath"`, `"editor.formatOnSave"`, `"[python]"`:
     - Với mỗi key bị thiếu, thêm `f"missing:{key}"` vào danh sách `errors`.
   - Sau khi kiểm tra thiếu key, nếu `"python.defaultInterpreterPath"` có mặt trong dict, kiểm tra giá trị của nó phải là `str` và không rỗng sau khi `.strip()`. Nếu không đạt, thêm `"invalid:python.defaultInterpreterPath"` vào `errors`.
   - Trả về `(len(errors) == 0, errors)`.
