Khi thử một prompt, bạn thường muốn đổi một setting chỉ cho một khối code, ví dụ `temperature` cao hơn, rồi lấy lại setting cũ, kể cả khi khối đó bị lỗi. Hãy viết context manager `temporary_setting(config, key, value)`. Bên trong khối `with`, `config[key]` bằng `value`. Khi khối kết thúc, setting trở về như trước. Viết code bên trong hàm, ví dụ bằng `@contextmanager` và `yield`.

**Ví dụ**

```python
config = {"model": "small"}
with temporary_setting(config, "model", "big"):
    print(config["model"])   # big
print(config["model"])       # small
```

**Quy tắc**
- Sửa trực tiếp dict bạn nhận được (người gọi phải thấy giá trị mới).
- Nếu `key` đã có trong `config`, hãy khôi phục giá trị cũ sau đó.
- Nếu `key` **chưa có** trong `config`, hãy xóa nó sau đó, để dict trông giống hệt như trước.
- Việc khôi phục cũng xảy ra khi khối raise lỗi, và lỗi đó vẫn phải đến tay người gọi (đừng giấu nó).
- Manager có thể lồng nhau: việc khôi phục phải trả về đúng giá trị đang có lúc manager này bắt đầu.
