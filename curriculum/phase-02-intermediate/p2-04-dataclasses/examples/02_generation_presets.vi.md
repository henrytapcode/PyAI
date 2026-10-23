# Các preset sinh văn bản

**Ví dụ này cho thấy:** một dataclass frozen có giá trị mặc định, dùng làm bộ cài đặt chỉ đọc. Các preset được lưu trong dict và mô tả bằng một method.

**Từng bước**
1. Dòng 5–9 định nghĩa `GenerationConfig`. `model` là bắt buộc; `temperature` và `max_tokens` có giá trị mặc định. `frozen=True` khiến mọi object đều chỉ đọc.
2. Dòng 11–19 thêm hai method. `describe` gọi `is_deterministic` qua `self`, điều này được phép vì dataclass là một class bình thường.
3. Dòng 22–26 tạo ba preset. Mỗi preset chỉ ghi ra những field khác với mặc định.
4. Dòng 28–29 duyệt dict và in mô tả của từng preset.
5. Dòng 31–35 thử đổi một giá trị. Object frozen từ chối, và nhánh `except AttributeError` chạy.
6. Dòng 38–40 tạo một config **mới** từ config cũ với temperature thấp hơn. Hai object khác nhau nên `==` cho ra `False`.

**Lưu ý:** "đổi" một object frozen nghĩa là tạo một object mới. Nhờ vậy bản gốc vẫn an toàn với những phần khác của chương trình đang dùng nó.

**Tự thử:** xóa `frozen=True` ở dòng 5. Dòng `config.temperature = 2.0` sẽ chạy được, và dòng `presets are read-only` không còn được in ra.
