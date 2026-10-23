# Tóm tắt một báo cáo lint

**Ví dụ này cho thấy:** các script CI thường đọc dạng ngắn của kết quả ruff. Chương trình này phân tích sáu dòng báo cáo và đếm số vấn đề theo mã rule và theo file.

**Từng bước**
1. Dòng 2–9 lưu báo cáo. Mỗi dòng có dạng `file:dòng:cột: MÃ thông báo`.
2. Dòng 12–15 cắt một dòng theo dấu `:` thành bốn phần, rồi tách phần cuối thành các từ. Từ đầu tiên là mã rule, và `"[*]" in words` là `True` khi ruff sửa được vấn đề.
3. Dòng 18–26 lặp qua báo cáo. `by_code.get(code, 0) + 1` là mẫu đếm: bắt đầu từ `0` ở lần đầu một mã xuất hiện.
4. Dòng 28–34 in các số đếm theo thứ tự đã sắp xếp, rồi in xem `--fix` sửa được bao nhiêu trong sáu vấn đề.

**Để ý:** các biến giữ số dòng và số cột bắt đầu bằng `_`. Đó là thói quen cho ý "mình tách giá trị này ra nhưng không cần dùng", và nó giúp các công cụ không báo tên không dùng.

**Tự thử:** thêm `"util.py:12:1: F401 [*] `re` imported but unused"` vào `REPORT`. `F401` giờ phải hiện `3`, và `fixable` phải là `3 of 7`.
