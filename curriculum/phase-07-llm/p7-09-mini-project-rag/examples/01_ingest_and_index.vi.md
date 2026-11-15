# Nạp tài liệu, chia chunk và truy xuất top-k

**Những gì ví dụ minh họa:** Chia kho 8 trang FAQ theo hai chiến lược câu và cửa sổ từ, index các chunk theo câu một lần bằng `FakeLLM(embed_dim=256)` rồi truy xuất top-2 bằng `np.argsort(-scores, kind="stable")`.

**Từng bước một**
1. Dòng 6–15 khai báo 8 trang FAQ của cửa hàng.
2. Dòng 18–37 định nghĩa `chunk_docs(raw_docs, mode, size, overlap)` để sinh các dict chunk mang ID `<source>#<n>`.
3. Dòng 40–43 in tổng số chunk mỗi cách (`24` chunk câu so với `33` chunk cửa sổ từ) kèm các ID đầu tiên.
4. Dòng 45–54 embed toàn bộ chunk câu một lần, embed câu hỏi bảo hành và in 2 chunk điểm cao nhất.

**Lưu ý:** Tách theo câu cho ít chunk hơn và sạch hơn (`24` so với `33`), giúp `warranty.md#0` đứng hạng `#1` (`0.625`) với trọn vẹn câu chứa `"12 months"`.

**Tự thử:** Đổi `sent_chunks` ở dòng 46 sang `word_chunks` để xem nội dung ở hạng `#1` bị cắt ra sao khi dùng cửa sổ 8 từ cố định.
