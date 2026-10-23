# Dùng `min` có sẵn với key

Cách này trước tiên tạo một list các row (tên và điểm trung bình), rồi để hàm `min(rows, key=...)` có sẵn chọn người thắng. Nó dùng cùng mẹo như `sorted`: hàm key trả về một tuple, và row có tuple nhỏ nhất sẽ thắng. `best_key` đổi dấu điểm trung bình, nên điểm cao nhất cho key nhỏ nhất; `worst_key` thì không đổi dấu. Cả hai đặt tên ở vị trí thứ hai, nên khi bằng điểm sẽ chọn tên đứng trước. `sum(row["avg"] for row in rows)` là cách viết gọn để cộng các điểm trung bình (xem trước một chủ đề ở bài sau).

Cách này ngắn hơn và nói rõ điều nó muốn ("giá trị nhỏ nhất theo key này"). Vòng lặp trong lời giải chính là cách tốt hơn để hiểu "người tốt nhất cho đến lúc này" hoạt động ra sao, và chỉ cần duyệt dữ liệu một lần.
