# Đọc pyproject.toml bằng tomllib

**Minh họa:** cách `uv` lưu thông tin dự án và dependency trong `pyproject.toml`, và cách Python 3.11+ đọc nó bằng `tomllib`.

**Từng bước**
1. Dòng 4–14 lưu một nội dung `pyproject.toml` mẫu dưới dạng chuỗi nhiều dòng.
2. Dòng 16 gọi `tomllib.loads(...)` để chuyển văn bản TOML thành các dictionary và list lồng nhau trong Python.
3. Dòng 19–23 đọc `name`, `requires-python`, và duyệt qua danh sách `dependencies`.

**Lưu ý:** `tomllib` có sẵn trong thư viện chuẩn của Python—bạn không cần `uv add` để đọc tệp `pyproject.toml`.

**Tự thử:** thêm `"pytest>=8.0"` vào `dependencies` rồi chạy lại.
