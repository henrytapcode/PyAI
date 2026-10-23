# Tóm tắt log

**Ví dụ này cho thấy:** ghi file bằng `"w"`, ghi thêm bằng `"a"`, rồi đọc từng dòng để đếm.

**Từng bước**
1. Dòng 2–3 import `tempfile` và `Path`. Dòng 5 tạo thư mục tạm, dòng 6 ghép đường dẫn `app.log` bên trong nó bằng `/`.
2. Dòng 8–10 mở file bằng `"w"` và ghi hai dòng. Mỗi dòng kết thúc bằng `\n`.
3. Dòng 11–13 mở lại bằng `"a"` và thêm hai dòng nữa. Không có gì bị xóa.
4. Dòng 16–22 duyệt qua file. `line.strip().split(" ")[0]` bỏ ký tự xuống dòng, cắt dòng thành các từ và giữ từ đầu tiên, tức mức log.
5. Dòng 24–25 in tên file cùng đuôi file, rồi in dict đếm.

**Lưu ý:** phải có `if level in counts` vì key phải tồn tại thì mới `+= 1` được.

**Thử tự làm:** đổi `with` thứ hai từ `"a"` thành `"w"` rồi chạy lại. Chỉ còn hai dòng cuối nên kết quả thành `{'INFO': 2}`.
