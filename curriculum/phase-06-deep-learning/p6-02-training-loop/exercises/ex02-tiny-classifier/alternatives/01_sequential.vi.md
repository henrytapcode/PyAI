# Nối các tầng bằng `nn.Sequential`

Thay vì lưu từng tầng vào một thuộc tính riêng (`self.hidden`, `self.relu`, `self.out`) rồi gọi lần lượt trong `forward`, cách viết này gom chuỗi Linear-ReLU-Linear vào một khối `nn.Sequential` duy nhất. `nn.Sequential` gọn và ít lặp code hơn khi dữ liệu chỉ đi thẳng một mạch qua danh sách các tầng mà không rẽ nhánh. Ngược lại, hãy tự viết `forward` tường minh bất cứ khi nào mô hình cần kết nối tắt (skip connection), nhiều đầu vào/đầu ra, hoặc rẽ nhánh có điều kiện giữa các tầng.
