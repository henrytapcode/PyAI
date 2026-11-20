# Review phase 5 (reviewer subagent, 2026-11-14)

Tổng: 1 blocker, 10 major, 27 minor. Boss đã xác minh: B1, M1, M7, M9 (và M2 là sự thật của `load_breast_cancer`: 1 = benign).
Nguyên nhân B1 nằm một phần ở spec boss viết cho p5-03 §6 ("chọn theo test score").

## Blocker
- **B1** Mâu thuẫn "chọn mô hình/ngưỡng bằng test": p5-02 quiz q15; p5-03 lesson §6 + Recap + quiz q15 + f06 + examples/03 + ex02 `best_model`; p5-04 lesson §5 + examples/02 (quét ngưỡng trên test) — trái với p5-05 §5, Mistake 2, q01, q13, f02, f03, glossary `holdout set`. Sửa: p5-03 §6 nói test dùng để so sánh minh họa một lần chia, chọn thật dùng CV trên train, test chấm một lần; p5-04 §5/ex02 thêm WARNING (hoặc quét trên validation tách từ train); p5-02 q15 sửa giải thích.

## Major
- **M1** `zero_division`: trên sklearn 1.7, F1/recall với dự đoán toàn 0 (khi có dương thật) **không** cảnh báo; chỉ precision cảnh báo khi TP+FP=0 (boss đã chạy). Sửa lý do ở p5-05 lesson "New in this lesson" + §4, quiz q07/q08/f04, ex02 prompt; p5-04 Mistake 1 + Recap.
- **M2** p5-04 examples/03 `load_breast_cancer`: lớp 1 = benign (đa số) → F1/recall đo lớp lành. Dùng `y = 1 - y` hoặc ghi rõ.
- **M3** VI: "độ chính xác" dùng cho cả accuracy (p5-02 dòng 78, glossary ~1322, p5-03 ex02 hint 2 VI, p5-05 bảng honest) và precision (p5-04 dòng 86, glossary ~1586); "độ phủ" (recall) đụng "độ phủ test". Thống nhất: accuracy = "tỉ lệ đoán đúng", precision/recall giữ tiếng Anh + giải nghĩa ("độ chuẩn khi báo dương", "độ nhạy / tỉ lệ bắt được").
- **M4** p5-05 VI §2: "chuyển ca trực" sai nghĩa escalate; "cột hậu kiểm" gượng → "cột chỉ có sau khi biết kết quả".
- **M5** Hint 2 là code (lộ lời giải): p5-01 ex02, p5-02 ex01, p5-02 ex02 (+ TODO starter `accuracy` ghi nguyên thân hàm).
- **M6** p5-05 ex01 hint 3 lộ ~60% lời giải.
- **M7** p5-01 ex02 test chấp nhận gradient thiếu hệ số 2 (boss chạy mutant: 6/6 qua). Thêm test giá trị chính xác sau 1–2 bước.
- **M8** p5-04 quiz q09 lộ đáp án trong đề.
- **M9** p5-03 examples/01 Try `[95.0, 5.0]` không đổi dự đoán (coef links âm; boss đã chạy).
- **M10** p5-05 examples/03 Try recall 0.90 rơi về mặc định 0.5 im lặng, nhãn vẫn ghi 0.80; "line 64" → 65.

## Minor (27, tóm tắt)
1. p5-04 §5 + ex02: "precision stays at 0.889" → giảm nhẹ từ 1.0.
2. p5-04 §5 + glossary decision threshold: "predict so với 0.5" chỉ đúng cho LogisticRegression nhị phân.
3. p5-03 §5/Recap: "leakage impossible / zero leakage" nói quá → chặn rò rỉ thống kê scaling.
4. p5-03 Recap: LogReg "cần" scaling mâu thuẫn §1.
5. p5-03 §1: R² thêm 1 câu (0 = không hơn đoán trung bình, có thể âm); thêm R² vào glossary.
6. p5-04 §6: câu StratifiedKFold làm tưởng `scoring` là tham số của nó.
7. p5-04 Mistake 3: lỗi và bản đúng ra cùng số → đổi cấu hình hoặc thành NOTE.
8. p5-02 Mistake 2: `clean test: [1.5, 4.5]` ngoài [0,1] chưa giải thích.
9. p5-02 examples/03: dữ liệu parabol, bậc 2 tốt hơn bậc 3 "sweet spot".
10. p5-03 examples/03: thắng 1/45 mẫu; dẫn sang CV; Try `max_depth=None` giải thích.
11. Line refs lệch 1–2 dòng: p5-01 ex/03, p5-04 ex/01–02 (Try "line 31" → 30), p5-05 ex/01–03.
12. p5-01 examples/03 Try lr=0.1 phát nổ, nói trước.
13. p5-02 examples/02.en Try "IDs stay small" sai nghĩa.
14. API chưa giới thiệu: `np.argmin` (p5-01 §3), `rng.normal` (p5-02 §5), `np.bincount` (p5-03 §2), `rng.integers/uniform`, `np.concatenate`, `np.column_stack` (p5-03 §4), `np.unique` (hint p5-02 ex02), `sklearn.base.clone` (prompt p5-03 ex02).
15. p5-02: lesson §4 lấy đầu permutation làm train, ex01 lấy đầu làm test.
16. Độ dài: lesson ~2000–2300 từ; p5-05 ~3700 từ, generator chép nhiều lần, dùng API chưa dạy.
17. p5-01 ex01 hint 3 trùng starter.
18. p5-02 ex02: test hòa với scores đã sắp; scores rỗng solution vs alternative khác nhau.
19. p5-03 ex02 `test_all_models_use_same_split` không kiểm "split once".
20. p5-04 ex02: hint 3 gần đủ lời giải + biến chết `best`; prompt EN câu zero denominator khó hiểu; comment test sai ngữ pháp.
21. p5-05 ex02 test boundary dùng 0.80 − 0.70 (float) không kiểm được "<" strict.
22. p5-05 ex01: không test phân biệt thứ tự dedup/dropna.
23. Fill nhiều đáp án hợp lệ: p5-03 q08 (`fit_transform`), p5-04 q04 (`0.0`, `prior`), p5-05 q08 (`0.0`), p5-05 q03 (dtype lộ trong đề).
24. Độ khó: p5-01 q14 gắn 3 quá cao; p5-05 chỉ 3 câu dễ.
25. VI gượng: p5-01 dòng 117 "mặt phẳng", "bảng vết" (p5-01 186, p5-02 95), p5-04 dòng 317 "lệch chuẩn", p5-05 dòng 28 "chuẩn hóa", Recap p5-05; p5-03 ex01 hint 2 VI "bộ phân loại hồi quy logistic".
26. p5-04 lesson.vi header bảng chưa dịch; nhãn trong examples/*.vi.md không thống nhất giữa các bài.
27. Glossary: `data leakage` quá hẹp, `target leakage` "near 1.0", `holdout set` EN/VI lệch, `decision threshold` (minor 2), thiếu R².
