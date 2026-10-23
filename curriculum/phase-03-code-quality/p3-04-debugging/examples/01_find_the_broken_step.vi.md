# Tìm bước bị hỏng

**Ví dụ này cho thấy:** một bộ làm sạch văn bản ba bước cho kết quả sai với `"GPT-4"`. In giá trị sau mỗi bước sẽ cho biết bước nào làm hỏng nó.

**Từng bước**
1. Dòng 3–12 định nghĩa ba bước nhỏ: chuyển chữ thường, bỏ dấu câu, gộp khoảng trắng. Vòng lặp trong `remove_punctuation` chỉ giữ lại chữ cái và khoảng trắng (`isalpha()` là `True` với chữ cái).
2. Dòng 15–19 định nghĩa `run`, hàm áp dụng từng bước và in một checkpoint: tên bước và giá trị dưới dạng `repr`.
3. Lần chạy đầu cho thấy `lowercase` vẫn ổn, nhưng sau `remove_punctuation` thì `-4` đã biến mất. Bug nằm ở bước đó, nên hai bước còn lại có thể bỏ qua.
4. Dòng 27–28 định nghĩa lại `remove_punctuation` để nó giữ cả chữ số và dấu gạch ngang. Lần chạy thứ hai cho ra `'use gpt-4 now'`.

**Lưu ý:** bạn không phải đọc toàn bộ chương trình. Bạn chỉ so sánh hai checkpoint liền kề và tìm ra checkpoint sai đầu tiên.

**Thử tự làm:** thêm bước thứ tư `strip_stopwords` để bỏ từ `"now"`, rồi chạy lại. Checkpoint mới sẽ xuất hiện ở cuối, còn ba checkpoint đầu không đổi.
