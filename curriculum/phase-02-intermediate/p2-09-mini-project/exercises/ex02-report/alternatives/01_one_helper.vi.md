# Một hàm phụ, hai hàm lấy key

Hai hàm tính tổng lặp lại cùng một vòng lặp, chỉ có key là khác. Phiên bản này viết vòng lặp một lần trong `group_totals` và truyền "cách lấy key" vào dưới dạng một hàm (hàm cũng là giá trị). `max(totals, key=totals.get)` là cách có sẵn để tìm key tốt nhất: nó gọi `totals.get` trên từng key và trả về key có kết quả lớn nhất. Vì các key đã được sắp xếp, `max` trả về key đầu tiên trong các tổng bằng nhau, nên khi hòa vẫn chọn tên đứng trước.

Đây là thiết kế tốt hơn khi bạn dự đoán sẽ có thêm cách gom nhóm khác (theo ghi chú, theo tuần). Với ba hàm nhỏ, các vòng lặp thường của lời giải chính dễ đọc hơn với người mới.
