# Đếm tần suất từ với Counter

**Ví dụ này cho thấy:** một công cụ làm sẵn trong thư viện chuẩn làm đúng việc mà bạn đã tự code bằng tay ở bài về collection.

**Từng bước**
1. Dòng 2 import một cái tên, `Counter`, từ module `collections`.
2. Dòng 4 là một câu. Dòng 5 dùng `text.split()` để cắt nó thành list các từ.
3. Dòng 7 tạo bộ đếm trong một bước: `Counter(words)` chính là cả vòng lặp `counts.get(word, 0) + 1`. Nó hoạt động như một dict từ từ sang số lần.
4. Dòng 9 in cả bộ đếm, từ xuất hiện nhiều nhất đứng đầu. Dòng 10 đọc một số đếm như với dict: `4`. Dòng 11 hỏi một từ không có và nhận `0`, **không** bị `KeyError`.
5. Dòng 12 `most_common(2)` trả về list các tuple `(từ, số lần)` cho 2 số đếm lớn nhất.
6. Dòng 14–15 lặp qua các tuple đó và tách mỗi tuple thành `word` và `number`. Trong f-string, `:<4` đệm từ cho đủ 4 ký tự để các con số thẳng hàng.

**Để ý:** khi các từ hòa nhau (`sat` và `on` đều xuất hiện hai lần), Counter giữ thứ tự mà nó gặp chúng lần đầu.

**Tự thử:** thay `text` bằng một câu của bạn và in `counts.most_common(1)`.
