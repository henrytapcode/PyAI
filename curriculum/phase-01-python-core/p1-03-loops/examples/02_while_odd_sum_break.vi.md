# While, continue và break phối hợp

**Ví dụ này cho thấy:** vòng lặp `while True` cộng các số lẻ, bỏ qua số chẵn bằng `continue`, và tự dừng bằng `break`.

**Từng bước**
1. Dòng 2-3 tạo hai biến: `total` (biến tích lũy) và `number` (biến đếm mà vòng lặp sẽ thay đổi).
2. Dòng 4, `while True:`, nghĩa là "lặp mãi mãi", nên bên trong phải có chỗ gọi `break`.
3. Dòng 5 cộng 1 vào `number` ở đầu mỗi vòng: 1, 2, 3, ...
4. Dòng 6-7: nếu `number` là số chẵn, `continue` bỏ qua phần còn lại của vòng. Vì thế 2, 4, 6, 8 không xuất hiện trong kết quả.
5. Dòng 8 cộng số lẻ `number` vào `total`; dòng 9 in ra. Các tổng là 1, 4, 9, 16, 25.
6. Dòng 10-11: khi `total` vượt 20 (xảy ra ở `number = 9`, total 25), `break` kết thúc vòng lặp ngay.
7. Dòng 12 chạy sau vòng lặp và in `number` cuối cùng: 9.

**Để ý:** thứ tự rất quan trọng. `number += 1` nằm **trước** `continue`. Nếu nằm sau, số chẵn sẽ gặp `continue` mà không được tăng, và vòng lặp bị kẹt mãi mãi.

**Tự thử:** đổi `20` thành `50` và đoán xem vòng lặp dừng ở đâu. (Các tổng là các số chính phương 1, 4, 9, ..., nên nó dừng ở `number = 15` với total 64.)
