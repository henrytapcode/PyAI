# Nhật ký lệnh gọi: model, kiểm tra, lưu

**Ví dụ này cho thấy:** giai đoạn 1 của một tracker, nhưng cho việc khác: nhật ký các lệnh gọi LLM API. Một frozen dataclass chứa một lệnh gọi, một hàm kiểm tra nó, và cả nhật ký được lưu vào file JSON rồi đọc lại.

**Từng bước**
1. Dòng 8–13 định nghĩa `ApiCall` là một frozen dataclass với bốn field.
2. Dòng 16–22 định nghĩa `check_call`. Hàm raise `ValueError` ngay khi một quy tắc bị vi phạm, và không trả về gì khi mọi thứ ổn.
3. Dòng 25–28 định nghĩa `save_calls`. Hàm kiểm tra **tất cả** lệnh gọi trước, rồi mới ghi file bằng `write_text`.
4. Dòng 31–33 định nghĩa `load_calls`. `ApiCall(**record)` trải mỗi dict thành các keyword argument.
5. Dòng 42–47 lưu ba lệnh gọi vào một thư mục tạm, đọc lại và so sánh. Hai list chứa object dataclass bằng nhau khi mọi field bằng nhau.
6. Dòng 49–54 thử lưu một lệnh gọi có `0` token. Việc lưu bị từ chối, và file cũ không bị đụng tới.
7. Dòng 56–59 cho thấy object frozen không sửa được.

**Để ý:** lệnh gọi sai bị từ chối **trước khi** file bị đụng tới. Vì thế file vẫn còn 3 lệnh gọi.

**Tự thử:** trong lệnh gọi `bad`, đổi đối số cuối `0.0` thành `-1.0` và số token (đối số đứng trước nó) thành `10`. Hãy đoán thông báo (`cost must not be negative, got -1.0`).
