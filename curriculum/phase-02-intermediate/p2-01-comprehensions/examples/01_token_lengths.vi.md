# Độ dài prompt

**Ví dụ này cho thấy:** ba loại comprehension cơ bản trên cùng một list prompt: list các số, dict, và list đã lọc.

**Từng bước**
1. Dòng 2–7 tạo một list gồm bốn prompt.
2. Dòng 9 tạo list số từ của từng prompt. `p.split()` cắt prompt thành các từ và `len(...)` đếm chúng, nên output là `[3, 1, 5, 3]`.
3. Dòng 12 dùng ngoặc nhọn và `key: value` để tạo dict từ mỗi prompt sang số từ của nó. Dòng 13 tra cứu một phần tử.
4. Dòng 15 thêm `if` ở cuối, nên chỉ những prompt có ít nhất 3 từ được giữ lại.
5. Dòng 18 dùng `max` trên list ở dòng 9 để tìm số lớn nhất.

**Để ý:** kết quả của comprehension là một collection hoàn toàn mới. Bản thân `prompts` không hề thay đổi.

**Tự thử:** đổi `>= 3` ở dòng 15 thành `>= 5`. Chỉ còn lại đúng một prompt.
