# Config JSON và bộ dọn JSON Lines

**Ví dụ này cho thấy:** dùng `json.dump` / `json.load` cho file cấu hình, và một công việc dọn dữ liệu từng dòng trên dataset `.jsonl`.

**Từng bước**
1. Dòng 6–12 chuẩn bị một dict cấu hình và bốn mẫu huấn luyện, trong đó có một mẫu có response rỗng.
2. Dòng 19–22 lưu cấu hình bằng `json.dump` rồi nạp lại bằng `json.load`. `ensure_ascii=False` giữ nguyên chữ tiếng Việt.
3. Dòng 24–26 ghi dataset thô: mỗi mẫu một dòng `json.dumps(item) + "\n"`.
4. Dòng 29 mở file nguồn và file đích trong cùng một `with`.
5. Dòng 30–34 đọc từng dòng bằng `json.loads(line)` và chỉ ghi vào file sạch nếu response dài ít nhất `min_length` ký tự.
6. Dòng 36–38 in số lượng rồi in các prompt còn lại.

**Lưu ý:** ngưỡng lấy từ file cấu hình chứ không nằm trong code. Muốn đổi luật, bạn sửa dữ liệu chứ không sửa chương trình.

**Thử tự làm:** đặt `"min_length": 1` trong `config`. Response `"ok"` giờ đã đủ dài, nên bạn sẽ thấy `kept 3 of 4`.
