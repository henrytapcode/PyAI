# Cô lập môi trường ảo

**Minh họa:** vì sao hai dự án có thể giữ hai phiên bản khác nhau của cùng một gói, và cách kiểm tra từng môi trường so với danh sách yêu cầu.

**Từng bước**
1. Dòng 2–5 định nghĩa hai môi trường dự án tách biệt (`chatbot` và `evals`) cùng các phiên bản gói đã cài.
2. Dòng 7 đặt ra các phiên bản mục tiêu (`required`).
3. Dòng 9–16 kiểm tra riêng từng môi trường xem thiếu gói nào hoặc lệch phiên bản nào.

**Lưu ý:** `chatbot` có `pydantic` nhưng `httpx` cũ hơn; `evals` có đúng `httpx` nhưng thiếu `pydantic`. Hai môi trường hoàn toàn không ảnh hưởng lẫn nhau.

**Tự thử:** thêm `"pydantic": "2.6.0"` vào `"evals"` rồi chạy lại để thấy cả hai danh sách đều rỗng.
