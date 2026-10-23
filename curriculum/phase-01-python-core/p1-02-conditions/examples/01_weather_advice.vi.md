# Lời khuyên theo thời tiết

**Ví dụ này cho thấy:** chuỗi `if` / `elif` / `else` trong đó nhánh đúng đầu tiên được chạy, cùng một cặp `if` / `else` riêng dùng giá trị `bool`.

**Từng bước**
1. Dòng 2–3 lưu dữ liệu đầu vào: `temperature` (một `int`) và `is_raining` (một `bool`).
2. Dòng 5 hỏi `31 >= 35`. Kết quả là `False`, nên Python bỏ qua dòng 6 và đi tới `elif` kế tiếp.
3. Dòng 7 hỏi `31 >= 25`. Kết quả là `True`, nên dòng 8 chạy và `advice` thành `"Warm day"`. Các dòng 9–12 bị bỏ qua hoàn toàn, dù `31 >= 15` cũng đúng.
4. Dòng 14 in kết quả bằng f-string: `31 degrees: Warm day`.
5. Dòng 16 kiểm tra `is_raining`. Nó vốn đã là `bool` nên không cần so sánh gì thêm. Giá trị là `False`, nên `else` ở dòng 18 chạy và dòng 19 in `No umbrella needed`.

**Để ý:** các điều kiện `elif` đi từ nhiệt độ cao xuống thấp. Nếu dòng 9 (`>= 15`) đứng đầu, mọi ngày ấm đều bị gọi là "Mild day".

**Tự thử:** đổi `temperature` thành `10` và `is_raining` thành `True`. Hãy đoán cả hai dòng kết quả trước khi bấm Run.
