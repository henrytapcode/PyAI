# Tái hiện rồi mới sửa

**Ví dụ này cho thấy:** một hàm chia list thành các chunk bị mất phần tử. Báo cáo chỉ nói "một số tài liệu bị mất". Thu nhỏ input giúp tìm ra lời gọi nhỏ nhất bị sai, và lời gọi đó trở thành một test.

**Từng bước**
1. Dòng 2–3 định nghĩa `chunk` có bug: `range` dừng quá sớm, ở `len(items) - size + 1`.
2. Dòng 7–9 thử ba input, từ lớn đến nhỏ. Input đầu đúng, input thứ hai mất số `3`, và input thứ ba trả về `[]`.
3. Lời gọi sai nhỏ nhất là `chunk([1], 2)`. Một phần tử và kích thước chunk là 2 là đủ để thấy bug, và nó chỉ vào phần cuối của `range`.
4. Dòng 12–13 sửa lỗi: `range` phải chạy tới `len(items)`.
5. Dòng 17–21 giữ lại các trường hợp dưới dạng các dòng `assert`. Giờ chúng đều đạt, và sẽ thất bại nếu bug quay lại.

**Lưu ý:** cách sửa chỉ là một thay đổi nhỏ, nhưng việc tìm ra input sai nhỏ nhất mới là thứ khiến nguyên nhân dễ thấy.

**Thử tự làm:** thêm trường hợp `assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]`. Nó vẫn phải đạt.
