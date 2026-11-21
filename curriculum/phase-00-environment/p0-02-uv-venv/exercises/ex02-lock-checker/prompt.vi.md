Cài đặt hai hàm trong `starter.py` để kiểm tra sự cô lập của môi trường ảo và so sánh các bản chụp lockfile:

1. **`check_venv_isolation(envs: dict[str, dict[str, str]], project: str, package: str, expected_version: str) -> dict`**
   - `envs` ánh xạ tên mỗi dự án tới dictionary `{tên_gói: phiên_bản}` của dự án đó.
   - Trả về `{"ok": bool, "status": str, "installed": str | None}` theo các quy tắc sau:
     - Nếu `project` không có trong `envs`: `{"ok": False, "status": "unknown_env", "installed": None}`
     - Tra cứu `package` (không phân biệt hoa thường) trong `envs[project]`. Nếu thiếu: `{"ok": False, "status": "missing_package", "installed": None}`
     - Nếu phiên bản đã cài != `expected_version`: `{"ok": False, "status": "version_mismatch", "installed": installed_ver}`
     - Ngược lại: `{"ok": True, "status": "ok", "installed": installed_ver}`

2. **`diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]`**
   - So sánh hai ánh xạ lockfile `{tên_gói: phiên_bản}`.
   - Trả về `{"added": [...], "removed": [...], "changed": [...]}` với cả ba danh sách đều được sắp xếp tăng dần:
     - `"added"`: gói có trong `new_lock` nhưng không có trong `old_lock`
     - `"removed"`: gói có trong `old_lock` nhưng không có trong `new_lock`
     - `"changed"`: gói có ở cả hai nhưng chuỗi phiên bản đã thay đổi

Nhấn **Check** để chạy kiểm thử.
