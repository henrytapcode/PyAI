# Bảng tra cứu cho xếp loại

Thay vì bốn dòng `if`, cách này giữ các ngưỡng trong một list gồm các cặp `(minimum, letter)` rồi duyệt từ trên xuống. Cặp đầu tiên có minimum `<= avg` sẽ thắng; nếu không cặp nào thỏa thì kết quả là `"F"`. Vòng lặp `for minimum, letter in GRADE_TABLE` tách từng cặp ra, giống như `for key, value in d.items()`.

Cách này tốt hơn khi thang điểm có thể thay đổi hoặc dài thêm: bạn sửa một dòng dữ liệu thay vì sửa logic. Với chỉ năm loại, chuỗi `if` trong lời giải chính cũng tốt không kém và dễ đọc hơn một chút cho người mới.
