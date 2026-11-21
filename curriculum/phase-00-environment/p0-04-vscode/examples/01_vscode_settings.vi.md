# Cấu hình VS Code dưới dạng JSON

**Ví dụ này minh họa:** tạo, chuyển thành chuỗi JSON và đọc lại cấu hình `.vscode/settings.json` bằng module `json` của Python.

**Từng bước**
1. Dòng 3–8 tạo một `dict` Python chứa bốn thiết lập cốt lõi của VS Code cho `.venv` và Ruff.
2. Dòng 10 gọi `json.dumps(settings, indent=2)` để định dạng dictionary thành JSON dễ đọc (tự chuyển `True` của Python thành `true` của JSON).
3. Dòng 13–15 phân tích lại chuỗi JSON bằng `json.loads()` và kiểm tra `editor.formatOnSave` cùng mã formatter cho Python.

**Tự thử nghiệm:** đổi `"ruff.lineLength"` thành `88` rồi chạy lại để xem đầu ra JSON mới.
