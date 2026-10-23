# Ba kiểu vòng lặp for

**Ví dụ này cho thấy:** vòng lặp `for` qua `range()`, qua một chuỗi, và đếm ngược, cùng với mẫu tích lũy trong bài học.

**Từng bước**
1. Dòng 2 tạo biến tích lũy `total` và đặt bằng 0, **trước** vòng lặp.
2. Dòng 3 bắt đầu vòng lặp: `n` lần lượt nhận giá trị 1, 2, 3, 4, 5 (`range(1, 6)` dừng trước 6).
3. Dòng 4 cộng `n` vào `total`. Dòng 5 in cả hai giá trị, nên kết quả cho thấy `total` tăng dần: 1, 3, 6, 10, 15.
4. Dòng 6 không thụt lề, nên nó chỉ chạy một lần, sau khi vòng lặp đã kết thúc.
5. Dòng 8-9 lặp qua chuỗi `"AI"`: `letter` là `"A"`, rồi `"I"`.
6. Dòng 11-12 dùng `range(10, 0, -3)`: bắt đầu từ 10, mỗi lần trừ 3, dừng trước 0. Kết quả là 10, 7, 4, 1.

**Để ý:** biến của vòng lặp (`n`, `letter`, `step`) chỉ là một biến bình thường. Python tự gán giá trị cho nó ở đầu mỗi vòng.

**Tự thử:** bấm **Visualize** và xem `total` thay đổi ở dòng 4. Sau đó đổi `range(1, 6)` thành `range(1, 11)` và đoán tổng cuối cùng trước khi chạy (phải là 55).
