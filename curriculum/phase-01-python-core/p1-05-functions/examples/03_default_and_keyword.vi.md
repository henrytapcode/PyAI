# Tham số mặc định và keyword argument

**Ví dụ này cho thấy:** người gọi hàm có thể bỏ qua một tham số, hoặc truyền nó theo tên.

**Từng bước**
1. Dòng 2: `greeting="Hello"` cho tham số một **giá trị mặc định** (default value). Nếu người gọi không đưa giá trị, Python dùng `"Hello"`.
2. Dòng 10: `greet("Lan")` chỉ truyền `name`, nên `greeting` là `"Hello"`. Kết quả: `Hello, Lan!`.
3. Dòng 11: đối số thứ hai được ghép theo vị trí, nên `greeting` trở thành `"Hi"`.
4. Dòng 12: `greeting="Xin chao"` là **keyword argument** (đối số theo tên): ta nói rõ mình đang truyền cho tham số nào. Cách này dễ đọc và thứ tự không còn quan trọng.
5. Dòng 6–7 làm điều tương tự với `rate=0.1`. Dòng 13 dùng giá trị mặc định, dòng 14 ghi đè bằng `rate=0.2`. Kết quả là số `float` vì `price * rate` là `float`.

**Để ý:** tham số có giá trị mặc định (`greeting`, `rate`) đứng **sau** tham số không có. Python bắt buộc thứ tự này.

**Tự thử:** gọi `greet(greeting="Hey", name="Minh")`. Thứ tự của các keyword argument không quan trọng.
