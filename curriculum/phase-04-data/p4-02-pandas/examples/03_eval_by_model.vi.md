# Điểm eval theo từng mô hình

**Ví dụ này cho thấy:** cách gom nhóm theo mô hình bằng `groupby`, tính trung bình và số lượng bằng `.agg(...)`, rồi tìm mô hình tốt nhất.

**Từng bước**
1. Dòng 4–8 tạo DataFrame `evals` chứa điểm của ba mô hình trên hai tác vụ (`qa` và `code`).
2. Dòng 10 gom nhóm theo `"model"`, tính cả `"mean"` lẫn `"count"` trên cột `"score"`, rồi làm tròn 2 chữ số.
3. Dòng 11 sắp xếp bảng tóm tắt theo điểm trung bình giảm dần.
4. Dòng 14–16 lấy tên mô hình dẫn đầu từ `summary.index[0]` và điểm của nó từ `summary.iloc[0]["mean"]`.

**Để ý:** sau khi `groupby("model")`, tên các mô hình trở thành **index** của DataFrame, nên `summary.index[0]` trả về `"claude"` và `summary.iloc[0]["mean"]` đọc điểm trung bình ở hàng `0`.

**Tự thử:** hạ điểm `"code"` của `claude` ở dòng 7 từ `0.94` xuống `0.80` và xem `gpt-4o` vươn lên hạng nhất (`0.9` so với `0.84`).
