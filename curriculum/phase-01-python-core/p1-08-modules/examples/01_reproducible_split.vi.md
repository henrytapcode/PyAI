# Chia train/test có thể tái lập

**Ví dụ này cho thấy:** hai module trong thư viện chuẩn phối hợp với nhau: `random` để xáo trộn và `statistics` để tóm tắt số liệu. Đây cũng là ý tưởng khi bạn chia một dataset thật thành tập train và tập test.

**Từng bước**
1. Dòng 2–3 import hai module. `import statistics as st` đặt cho `statistics` một biệt danh ngắn, nên ta viết `st.mean(...)`.
2. Dòng 8–14 định nghĩa `split_scores`. Dòng 9 tạo một đối tượng `random.Random(seed)`: một bộ sinh số ngẫu nhiên riêng, bắt đầu từ con số bạn đưa vào. Cùng seed thì cùng chuỗi lựa chọn "ngẫu nhiên".
3. Dòng 10 sao chép list bằng `list(values)`, để việc xáo trộn không làm đổi `scores`. Dòng 11 xáo bản sao. Dòng 12–13 cắt thành phần test nhỏ và phần còn lại là train.
4. Dòng 17–18 gọi hàm hai lần với `seed=42`. Dòng 22 in `True`: hai lần gọi cho ra đúng cùng một cách chia.
5. Dòng 23–25 dùng `st.mean` và `st.stdev` (độ lệch chuẩn, cho biết các số phân tán đến mức nào) rồi làm tròn kết quả.

**Để ý:** các con số trông có vẻ ngẫu nhiên nhưng thật ra không. Chạy chương trình mười lần bạn vẫn nhận cùng một kết quả. Đó là điều làm thí nghiệm **tái lập được** (reproducible): đồng đội có thể lặp lại kết quả của bạn.

**Tự thử:** đổi `seed=42` thành `seed=7` ở cả hai lời gọi. Cách chia sẽ đổi, nhưng hai lời gọi vẫn khớp nhau.
