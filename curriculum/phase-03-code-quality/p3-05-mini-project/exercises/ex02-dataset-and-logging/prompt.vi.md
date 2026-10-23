Giờ đến nửa sau của bộ công cụ: làm sạch cả một list văn bản và báo cáo những gì đã xảy ra. `CleanConfig`, `clean_text` và `CleanReport` đã được viết sẵn trong trình soạn thảo. Hãy viết code bên trong `clean_dataset` và `return` báo cáo. Phần 5 của bài học cho thấy vòng lặp và phần logging.

**Ví dụ**

```python
report = clean_dataset(["Hi  there", "hi there", "", 7])
report.kept         # ["hi there"]
report.skipped      # 1   (con số 7)
report.empty        # 1   ("")
report.duplicates   # 1   ("hi there" lần thứ hai)
```

Lần chạy cũng ghi hai log record:

| level | thông báo |
|---|---|
| `WARNING` | `skipping item 3: not a string` |
| `INFO` | `kept 1 of 4 texts` |

**Quy tắc**
- Duyệt `texts` theo thứ tự. Đừng thay đổi list bạn nhận được.
- Một mục không phải string sẽ bị **bỏ qua**: log một `WARNING` `skipping item N: not a string` (N là vị trí của nó, bắt đầu từ 0) và đếm nó vào `skipped`.
- Làm sạch một string bằng `clean_text(item, config)`. Kết quả rỗng được đếm vào `empty`. Kết quả đã gặp trước đó được đếm vào `duplicates`. Mọi kết quả khác được thêm vào `kept`, theo thứ tự ban đầu.
- Đừng log từng văn bản rỗng hay trùng. Hãy log đúng **một** dòng tổng kết `INFO` ở cuối: `kept K of N texts`, trong đó `K` là số được giữ và `N` là độ dài của `texts`.
- Dùng `logger.warning(...)` và `logger.info(...)` với đối số `%d`, không dùng f-string.
