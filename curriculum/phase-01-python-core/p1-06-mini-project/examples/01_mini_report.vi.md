# Bảng điểm thu nhỏ

**Ví dụ này cho thấy:** toàn bộ project ở dạng thu nhỏ: hai hàm nhỏ, một list các dict và một vòng lặp nối chúng lại.

**Từng bước**
1. Dòng 2–5 định nghĩa `average`. Dòng 3 kiểm tra list rỗng trước, để không bao giờ chia cho 0. Dòng 5 cộng các điểm rồi chia cho số lượng.
2. Dòng 8–13 định nghĩa `letter_grade`. Python kiểm tra các dòng `if` từ trên xuống, dòng nào đúng đầu tiên sẽ `return`. Vì vậy mỗi dòng chỉ cần một phép so sánh.
3. Dòng 16–19 lưu dữ liệu: một list, mỗi học sinh là một dict. Mỗi dict có `"name"` và list `"scores"`.
4. Dòng 21 bắt đầu vòng lặp, mỗi lần một học sinh. Dòng 22 lấy điểm của học sinh đó bằng `student["scores"]` rồi tính trung bình.
5. Dòng 23 tạo dòng kết quả. `{avg:.2f}` hiển thị hai chữ số thập phân và `letter_grade(avg)` được gọi ngay trong f-string.

**Để ý:** `average` và `letter_grade` không biết gì về học sinh hay dict. Chúng chỉ nhận một số hoặc một list. Nhờ vậy bạn có thể kiểm thử riêng từng hàm và dùng lại ở bất kỳ đâu.

**Tự thử:** thêm `{"name": "Chi", "scores": [5, 6, 4.5]}` vào list. Hãy đoán dòng mới trước khi chạy (phải in ra `Chi: 5.17 (C or below)`).
