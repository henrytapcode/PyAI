# Lưu, nạp lại và xóa trong VectorStore

**Những gì ví dụ minh họa:** Tuần tự hóa `VectorStore` thành chuỗi JSON, nạp lại với 0 lần gọi `embed()`, rồi xóa một bản ghi mà không làm lệch vị trí các vector còn lại.

**Từng bước một**
1. Dòng 7–14 bọc `FakeLLM` trong `CountingClient` để đếm mọi lần gọi `embed()`.
2. Dòng 51–67 xuất `ids`, `texts`, `metadatas` và `vectors` ra JSON (`to_json`) rồi dựng lại store cùng ma trận NumPy trực tiếp từ các số thực đã lưu (`from_json`).
3. Dòng 70–83 thêm ba chunk (`1` lần gọi embed), nạp lại sang store mới (`0` lần gọi embed trong `from_json`), xác nhận kết quả search giống hệt, rồi gọi `delete("c2")` và thấy `c1` vẫn khớp đúng điểm `0.775`.

**Lưu ý:** `from_json()` chỉ dùng `reload_client` ở bước sau để embed câu hỏi mới `"money back for laptop"`, tiết kiệm toàn bộ chi phí embed lại kho tài liệu.

**Tự thử:** Xóa thêm `"c1"` rồi gọi `reloaded.search("cheap car", k=1)` để kiểm tra `"c3"` vẫn còn nguyên ở hàng `0`.
