Cài đặt hai hàm trợ giúp trong `starter.py` bằng thư viện chuẩn Python (`tomllib`):

1. **`parse_dependencies(toml_text: str) -> dict[str, str]`**
   - Phân tích `toml_text` bằng `tomllib.loads`.
   - Đọc `[project].dependencies` (trả về `{}` nếu thiếu `[project]` hoặc `dependencies`).
   - Với mỗi chuỗi dependency:
     - Hỗ trợ các toán tử `==`, `>=`, `<=`, `~=`, `!=`, `>`, `<`.
     - Xóa khoảng trắng quanh tên gói và quanh số phiên bản (ví dụ `"httpx >= 0.27.0"` thành `"httpx": ">=0.27.0"`).
     - Bỏ hậu tố `[extras]` tùy chọn khỏi tên gói (ví dụ `"requests[security]>=2.31"` thành `"requests": ">=2.31"`).
     - Chuyển tên gói về chữ thường (ví dụ `"PyYAML>=6.0"` → `"pyyaml": ">=6.0"`).
     - Nếu không có toán tử phiên bản (ví dụ `"pytest"`), ánh xạ tên gói tới `""`.

2. **`missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]`**
   - So sánh tên gói không phân biệt hoa thường.
   - Trả về danh sách đã sắp xếp tăng dần các tên gói viết thường có trong `required` nhưng chưa có trong `installed`.

Nhấn **Check** để chạy kiểm thử.
