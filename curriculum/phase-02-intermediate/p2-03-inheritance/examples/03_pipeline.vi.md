# Pipeline gồm nhiều model

**Ví dụ này cho thấy:** composition. `Pipeline` không phải một model; nó có một list model và cho văn bản đi qua theo thứ tự.

**Từng bước**
1. Dòng 2-26 định nghĩa họ model: `Model` cha và ba class con (`EchoModel`, `ShoutModel`, `TagModel`).
2. Dòng 29-31 định nghĩa `Pipeline`. `__init__` chỉ lưu list vào `self.steps`. Nó không kế thừa từ ai cả.
3. Dòng 33-34: `add` thêm một model vào cuối list.
4. Dòng 36-40: `run` cho văn bản đi qua từng bước. Đầu ra của bước này thành đầu vào của bước sau, và sau mỗi bước có một dòng được in ra.
5. Dòng 43-48 dựng pipeline hai bước, thêm bước thứ ba, chạy nó, và cho thấy pipeline không phải là `Model`.

**Để ý:** dòng cuối in `False`. `Pipeline` có model nhưng không phải là model, nên `isinstance` trả lời không.

**Tự thử:** chuyển `TagModel` lên đầu list ở dòng 43 (và xóa dòng `add`). Kết quả đổi mà không cần viết class mới.
