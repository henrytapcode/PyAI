Chuỗi `DOCKERFILE` trong `starter.py` dùng để đóng gói một dịch vụ FastAPI, nhưng đang mắc **bốn lỗi** khiến cả bốn bài kiểm tra đều fail:

1. **Base image không cố định phiên bản** (`test_base_image_pins_a_specific_tag` fail): các lần build sau có thể âm thầm kéo bản Python mới hơn.
2. **Thứ tự lệnh làm trượt build cache** (`test_copies_requirements_before_installing_then_app_code` fail): chỉ sửa code ứng dụng cũng làm bước cài thư viện phải chạy lại từ đầu.
3. **Layer cài gói bị phình dung lượng** (`test_pip_install_uses_no_cache_dir` fail): các file `.whl` tải về vẫn nằm lại bên trong layer của image.
4. **Không nhận kết nối từ máy host** (`test_cmd_uses_exec_form_and_binds_all_interfaces` fail): request chuyển tiếp từ máy host qua `-p 8000:8000` bị container từ chối.

Hãy sửa trực tiếp chuỗi `DOCKERFILE` trong `starter.py` để vượt qua cả bốn kiểm tra.

**Ví dụ**

```text
test_base_image_pins_a_specific_tag                       -> PASSED
test_copies_requirements_before_installing_then_app_code -> PASSED
test_pip_install_uses_no_cache_dir                       -> PASSED
test_cmd_uses_exec_form_and_binds_all_interfaces         -> PASSED
```

**Quy tắc**
- Giữ `DOCKERFILE` là chuỗi nhiều dòng trong code (không chạy lệnh `docker`).
- Giữ `WORKDIR /app`, `EXPOSE 8000`, bước cài `requirements.txt` và `uvicorn main:app` ở cổng `8000` dạng mảng JSON exec form.
- Khắc phục đủ bốn triệu chứng nêu trên để image lặp lại được, tận dụng build cache, gọn nhẹ và truy cập được từ máy host.
