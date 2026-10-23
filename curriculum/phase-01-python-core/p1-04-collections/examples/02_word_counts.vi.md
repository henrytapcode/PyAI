# Đếm từ

**Ví dụ này cho thấy:** cách dùng dictionary để đếm, và cách đọc lại bằng `[]`, `.get()` và `.items()`.

**Từng bước**
1. Dòng 2 là dữ liệu: 7 từ, có từ lặp lại. Dòng 4 bắt đầu với một dict rỗng.
2. Vòng lặp ở dòng 5–9 đi qua từng từ. Nếu từ đã là một key (dòng 6) thì cộng 1 vào số đếm. Ngược lại (dòng 8) đây là lần đầu thấy từ này, nên lưu `1`.
3. Dòng 11 in cả dict. Các từ giữ thứ tự xuất hiện lần đầu.
4. Dòng 12 đọc một số đếm bằng `[]`: `3`.
5. Dòng 13 hỏi một từ không có trong dict. `.get("python", 0)` trả về `0` thay vì gây lỗi `KeyError`.
6. Dòng 14–15 lặp qua `counts.items()`, tách mỗi cặp thành `word` và `n`.

**Để ý:** đây là bản dài của `counts[word] = counts.get(word, 0) + 1` trong bài. Hai cách làm cùng một việc. Hãy thử xem dòng 6–9 trở thành một dòng đó như thế nào.

**Tự thử:** thêm `"python"` vào cuối `words` rồi chạy lại. `counts.get("python", 0)` giờ in ra `1`.
