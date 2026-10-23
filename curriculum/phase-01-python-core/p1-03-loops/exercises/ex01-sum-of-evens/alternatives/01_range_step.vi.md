# Để range tự bỏ qua số lẻ

Thay vì kiểm tra từng số bằng `if number % 2 == 0`, hãy bắt đầu từ 2 và dùng `step = 2`: `range(2, n + 1, 2)` chỉ tạo ra 2, 4, 6, ... nên mọi số đều đã là số chẵn. Không cần `if` nào, và vòng lặp chỉ làm một nửa việc. Ý tưởng vẫn là mẫu tích lũy; bạn chỉ đổi những số mà vòng lặp đi qua.
