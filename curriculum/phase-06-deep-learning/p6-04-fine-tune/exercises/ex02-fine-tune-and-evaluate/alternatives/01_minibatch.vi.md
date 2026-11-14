# Fine-tune bằng mini-batch DataLoader

Thay vì chạy một bước full-batch duy nhất mỗi epoch trên toàn bộ ticket train, cách này bọc các tensor đã tokenize vào `TensorDataset` rồi duyệt bằng `DataLoader(..., batch_size=8, shuffle=True, num_workers=0, generator=...)`, cập nhật trọng số sau từng mini-batch và trả về loss trung bình của các batch mỗi epoch.

Chia mini-batch tốn ít bộ nhớ hơn và thực hiện nhiều bước cập nhật hơn mỗi epoch khi dữ liệu lớn hơn vài chục câu, còn cách full-batch ở `solution.py` thì gọn nhẹ và đủ nhanh cho tập dữ liệu nhỏ trên CPU.
