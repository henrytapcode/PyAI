# Bỏ qua phụ âm bằng continue

Ở đây `if` được đảo ngược: khi chữ cái **không** phải nguyên âm thì `continue` nhảy sang chữ kế tiếp, và chỉ nguyên âm mới đến được `count += 1`. Hai cách cho cùng kết quả. Với phép kiểm tra đơn giản như này, cách gốc dễ đọc hơn; `continue` có lợi khi thân vòng lặp dài và bạn muốn loại bỏ sớm những phần tử không cần.
