# Đọc mẫu bản VI phase 6–8 (reviewer Opus, 2026-11-18)

Mẫu (~25%): lesson.vi.md của p6-02, p7-03, p7-07, p8-03, p8-05; prompt.vi.md của p6-02 ex02, p7-03 ex02, p7-07 ex02, p8-03 ex01, p8-05 ex02; phần `vi:` quiz của 5 bài đó. Chưa sửa gì.

## Điểm tự nhiên (1–5)
p6-02 4 · p7-03 3.5 (sát chữ nhất) · p7-07 4 · p8-03 4.5 · p8-05 4. Prompt và quiz phần lớn ổn.

## Nặng
- p7-03 lesson.vi.md:310: "độ dài văn bản" → phải là "độ dài vector".
- p7-07 lesson.vi.md:332: thêm "(hoặc `max_steps`)" làm ngược ý EN (`repeat` dừng ngay thay vì quay tới `max_steps`); bỏ "Giới hạn là rất rõ".
- p6-02 lesson.vi.md:436: thiếu ý "validation lớn hết bộ nhớ"; "không làm sai số dự đoán" dễ nhầm thuật ngữ.

## Vừa
- p7-03 l.33 "Cần nói thật…" (thiếu "tất định"); l.291 "thắng về tích vô hướng"; l.145 `kind="stable"`; l.336 "giữ đồng nhất model cùng số chiều"; ex02 prompt l.20 "nhỏ hơn hẳn `min_score`" → `score < min_score` (bằng ngưỡng thì giữ).
- p7-07 l.5 "chạy một hàm model đề xuất" → "chạy hàm mà model đề xuất".
- p6-02 l.59 bị động "sẽ được bạn dùng".
- p8-03 l.448 "đóng băng mẫu đầu tiên".
- p8-05 l.682 "nối dây"; l.368 "Giờ đo `t0 = clock()`…".

## Nhẹ
p6-02 l.203 "giảm vọt" → "tụt mạnh", l.1; p8-05 l.22 cột "part", l.254 "nhảy trước" → "tua nhanh"; p8-03 l.326 gloss lặp, l.206 "đụng hàng"; p7-03 l.129, l.223; p6-02 ex02 prompt l.4, l.21.

## Lỗi lặp (sửa hàng loạt)
1. Xưng "ta"/"chúng ta" (guide chỉ dùng "bạn"): p6-02:7,311,371 (+ examples/03_save_and_reload.vi.md:12); p7-03:1,30,37,90; p7-07:241; p8-05:43,254; ngoài mẫu p6-03:170, p6-04:167/273/277, p7-01:194, p7-04:38, p7-05:219/259, p7-06:101/226, p7-08:174/176/356, p7-10:234/722 + alternatives 01_dataclass_registry, p8-04:7/94/124/139. Grep `(^|[ .:])(Ta|ta|chúng ta) ` trong `*.vi.md`, bỏ "người ta".
2. "accuracy" để trần: p6-02 l.371, quiz p6-02-q13, q15 → "tỉ lệ đoán đúng (accuracy)".
3. "độ chính xác": p7-04 lesson:498, quiz:298/388; p7-10 quiz:199 → với ANN dùng "độ nhạy (recall)". p6-01 (precision số thực) giữ.
4. Dịch sát thành ngữ: wiring→"nối dây", sample→"mẫu", wins→"thắng", be honest→"nói thật", jump forward→"nhảy trước".
