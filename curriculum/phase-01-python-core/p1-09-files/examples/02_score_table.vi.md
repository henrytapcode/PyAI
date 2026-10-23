# Bảng điểm trong CSV

**Ví dụ này cho thấy:** vòng đi-về đầy đủ của CSV: ghi các dòng bằng `DictWriter`, đọc lại bằng `DictReader`, đổi chữ thành số và tính trung bình.

**Từng bước**
1. Dòng 6–11 mô tả dữ liệu bằng một list các dict. Mỗi dict là một dòng.
2. Dòng 16–19 ghi file. `writeheader()` ghi dòng `name,score`, còn `writerows(rows)` ghi mỗi dict thành một dòng.
3. Dòng 23–32 đọc lại. `csv.DictReader(f)` cho ra một dict mỗi dòng, dùng dòng header làm key.
4. Dòng 26 dùng `float(row["score"])` vì giá trị CSV luôn trả về dạng chữ.
5. Dòng 34–35 in điểm trung bình của từng học sinh với hai chữ số thập phân.

**Lưu ý:** cả hai lần `open` đều truyền `newline=""`. Module `csv` cần điều này, nếu không trên Windows bạn có thể bị dòng trống.

**Thử tự làm:** thêm `{"name": "An", "score": 10}` vào `rows` rồi chạy lại. Một dòng mới `An: 10.00` sẽ xuất hiện ở cuối.
