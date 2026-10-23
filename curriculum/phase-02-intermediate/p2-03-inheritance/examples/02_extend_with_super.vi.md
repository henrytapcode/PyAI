# Model đếm số lần được gọi

**Ví dụ này cho thấy:** class con giữ nguyên hành vi của cha và thêm một chút bên trên, dùng `super()` ở ba chỗ.

**Từng bước**
1. Dòng 14-16: `__init__` gọi `super().__init__(name)` để `self.name` tồn tại, rồi thêm `self.calls = 0`.
2. Dòng 18-20: `generate` cộng 1 vào `self.calls`, rồi trả về `super().generate(prompt)`. Phần việc thật vẫn nằm ở class cha.
3. Dòng 22-23: `describe` lấy chuỗi của cha và thêm số lần gọi vào cuối.
4. Dòng 26-30 tạo object, in mô tả, gọi `generate` ba lần, rồi in mô tả lần nữa. Số đếm đã đi từ 0 lên 3.

**Để ý:** class con không lặp lại code của cha. Nếu `Model.generate` thay đổi, `CountingModel` được hưởng luôn.

**Tự thử:** sửa vòng lặp để có bốn câu hỏi. Dòng cuối sẽ là `calls so far: 4`.
