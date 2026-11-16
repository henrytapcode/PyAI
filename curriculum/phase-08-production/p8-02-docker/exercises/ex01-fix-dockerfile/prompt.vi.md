Chuỗi `DOCKERFILE` trong `starter.py` dùng để đóng gói một dịch vụ FastAPI, nhưng đang mắc bốn lỗi phổ biến: base image chưa ghim tag, thứ tự layer làm mất build cache, thiếu cờ bỏ cache khi `pip install` và bind nhầm `127.0.0.1` khiến máy host không gọi được vào container. Hãy sửa trực tiếp chuỗi `DOCKERFILE` để vượt qua cả bốn bài kiểm tra.

**Ví dụ**

```text
FROM python:3.13-slim
...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Quy tắc**
- Giữ `DOCKERFILE` là chuỗi nhiều dòng trong code (không chạy lệnh `docker`).
- Ghim `FROM` vào một tag Python cụ thể (không dùng `latest` hay bỏ trống tag).
- Đặt `COPY requirements.txt .` trước `RUN pip install`, và đặt `RUN pip install` trước `COPY . .`.
- Thêm `--no-cache-dir` vào lệnh `pip install`.
- Giữ `CMD` ở dạng mảng JSON exec form (`[...]`) và bind `--host 0.0.0.0`.
