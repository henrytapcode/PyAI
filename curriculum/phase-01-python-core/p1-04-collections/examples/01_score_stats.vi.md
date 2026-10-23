# Thống kê điểm số

**Ví dụ này cho thấy:** bộ đồ nghề thường dùng với list trên cùng một list: `append`, indexing, slicing, vòng lặp `for` với accumulator, `sorted` và `in`.

**Từng bước**
1. Dòng 2 tạo một list gồm ba điểm của mô hình. Dòng 3 thêm điểm thứ tư bằng `.append`, nên list giờ có 4 phần tử.
2. Dòng 5 in `len(scores)`, tức là `4`. Dòng 6 in phần tử đầu (`scores[0]`) và phần tử cuối (`scores[-1]`).
3. Dòng 7 cắt từ index 1 đến trước index 3. Đó là phần tử thứ 2 và thứ 3: `[0.91, 0.78]`.
4. Dòng 9–11 là mẫu accumulator: `total` bắt đầu bằng `0` và mỗi điểm được cộng dồn vào đó.
5. Dòng 12–13 chia cho số lượng điểm để ra trung bình, rồi `round(average, 3)` giữ lại 3 chữ số thập phân.
6. Dòng 14 in một bản sao đã sắp xếp. `scores` gốc không bị đổi. Dòng 15 hỏi `0.91` có trong list không: `True`.

**Để ý:** slice `scores[1:3]` chỉ có 2 phần tử, không phải 3. Index `stop` không bao giờ được lấy.

**Tự thử:** sửa dòng 7 thành `scores[:2]` và đoán kết quả trước khi chạy (hai điểm đầu: `[0.82, 0.91]`).
