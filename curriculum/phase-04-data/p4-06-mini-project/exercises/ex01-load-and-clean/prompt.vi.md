Viết hàm `load_and_clean(csv_text)` để biến chuỗi CSV log API chatbot thô thành một pandas `DataFrame` sạch. Hãy viết code bên trong hàm và `return` về `DataFrame` đã làm sạch.

**Ví dụ**

`csv_text` đầu vào:

```text
request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r01,gpt_4o,999,900,error,1
r02,mini,,N/A,ok,9
```

`DataFrame` trả về:

```text
  request_id   model  tokens  latency_ms status  rating
0        r01  gpt-4o    1200       850.0     ok     5.0
```

**Quy tắc**

- Trả về các cột theo đúng thứ tự: `["request_id", "model", "tokens", "latency_ms", "status", "rating"]`.
- Chuẩn hóa cột `model` bằng `.strip()`, `.lower()` và thay `"_"` thành `"-"`.
- Chuyển `model` và `tokens` bằng `.astype(str)` trước khi gọi `.str` để dữ liệu toàn số hoặc toàn ô trống không gây `AttributeError`.
- Chuyển `tokens` sang số bằng cách bỏ dấu phẩy `","` và ép kiểu an toàn, sau đó loại các dòng trùng `request_id` (giữ dòng đầu `keep="first"`), bỏ các dòng thiếu `tokens`, đánh lại index `0..n-1` rồi ép `tokens` sang kiểu `"int64"`.
- Ép `latency_ms` và `rating` sang `"float64"` (giá trị lỗi hoặc trống thành `NaN`), và biến mọi `rating` nằm ngoài khoảng `1..5` thành `NaN`.
- Nếu mọi dòng đều hỏng (hoặc CSV chỉ có dòng tiêu đề), trả về `DataFrame` rỗng vẫn đủ 6 cột đúng thứ tự và cột `tokens` có dtype `"int64"`.
