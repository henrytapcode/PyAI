# M4 bước 27b: sửa bản tiếng Việt phase 6–8 theo đọc mẫu

## Mục tiêu
Sửa các lỗi trong `tasks/m4-vi-sample-review.md`: 3 lỗi nặng, các lỗi vừa và nhẹ đã nêu, và 4 lỗi lặp trên **toàn bộ** phase 6–8 (không chỉ trong mẫu).
- Chỉ sửa câu chữ tiếng Việt. Không đổi ý, không đổi code, không đổi đáp án.
- Bản VI phải khớp ý bản EN.

## File được phép sửa
- Trong `curriculum/phase-06-deep-learning/**`, `curriculum/phase-07-llm/**`, `curriculum/phase-08-production/**`:
  - mọi file `*.vi.md` (lesson, examples, prompt, alternatives);
  - phần `vi:` trong `quiz.yaml`, `exercise.yaml` (hint), `phase-test.yaml`.
- `tasks/m4-vi-fixes.report.md`

## Không được đụng
- Mọi file `*.en.md`, mọi file `.py`, `.out`, `meta.yaml`, phần `en:`, `answer`, `code`, `lines` trong YAML.
- `tools/**`, `apps/**`, `packages/**`, `docs/**`, glossary, syllabus, topics, các phase khác.
- Trong code block của file `.vi.md`: chỉ được sửa `#` comment, và comment ngay sau `print(...)` là output, **không** được sửa.
- Không đổi số dòng của mermaid, không đổi text fence, không đổi thứ tự callout.

## Việc cần làm

### 1. Lỗi nặng (sửa đúng như đề xuất trong report, có thể chỉnh câu cho tự nhiên)
- `phase-07-llm/p7-03-embeddings/lesson.vi.md` ~l.310: "độ dài văn bản" → "độ dài vector".
- `phase-07-llm/p7-07*/lesson.vi.md` ~l.332: viết lại cho khớp EN. Phanh `repeat` dừng vòng lặp ngay, **không** để agent quay vòng tới `max_steps`. Bỏ "Giới hạn là rất rõ".
- `phase-06-deep-learning/p6-02-training-loop/lesson.vi.md` ~l.436: bổ sung ý "cho tới khi một lượt validation lớn bị hết bộ nhớ", và tránh cụm "sai số dự đoán".

### 2. Lỗi vừa và nhẹ
Sửa từng mục ở các phần "Vừa" và "Nhẹ" của `tasks/m4-vi-sample-review.md`. Số dòng chỉ là gần đúng; tìm theo câu trích.

### 3. Lỗi lặp, sửa trên toàn phase 6–8
1. **Xưng hô:** bỏ "ta"/"chúng ta", dùng "bạn" hoặc câu không chủ ngữ.
   Tìm bằng lệnh dưới đây và bỏ qua "người ta":
   `grep -rnE "(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) " curriculum/phase-0[678]* --include=*.vi.md`
   Làm tương tự với `--include=*.yaml`, chỉ trong phần `vi:`.
   Kết quả sau khi sửa phải là 0 dòng, trừ "người ta" và chữ "ta" thuộc từ khác.
2. **accuracy:** ở phần văn VI (không phải code), "accuracy" đứng trần thì viết "tỉ lệ đoán đúng (accuracy)" ở lần đầu trong mỗi file, các lần sau được để "tỉ lệ đoán đúng". Ví dụ: p6-02 lesson ~l.371, quiz p6-02-q13, q15.
3. **"độ chính xác":** grep trong phase 6–8.
   - Với ANN hay tìm kiếm gần đúng (p7-04 lesson ~l.498, quiz ~l.298/388; p7-10 quiz ~l.199), đổi thành ý "độ nhạy (recall)": đánh đổi một chút recall, có thể sót vài kết quả gần nhất.
   - Chỗ nói độ chính xác của số thực (float32 precision, p6-01) thì giữ.
   - Chỗ khác thì xét theo nghĩa EN và ghi quyết định vào report.
4. **Dịch sát thành ngữ:** dò toàn phase 6–8 các cụm "nối dây", "đóng băng mẫu", "thắng về", "nói thật", "nhảy trước", "đụng hàng". Viết lại cho tự nhiên (ví dụ: "lắp ráp", "giữ cứng câu trả lời ngẫu nhiên đầu tiên", "vượt lên", "nói rõ", "tua nhanh", "trùng nhau").

## Tiêu chí hoàn thành (checklist)
- [ ] 3 lỗi nặng đã sửa, khớp EN
- [ ] Mọi mục Vừa và Nhẹ trong report đã sửa, hoặc ghi lý do không sửa
- [ ] grep "ta"/"chúng ta" trên phase 6–8 ra 0 dòng (trừ "người ta")
- [ ] "độ chính xác" chỉ còn ở chỗ nói precision của số thực
- [ ] Không file `.en.md`/`.py`/`.out` nào bị sửa; phần `en:` trong YAML không đổi
- [ ] Validate phase 6–8 0 lỗi
- [ ] Report có bảng: file → số chỗ sửa theo nhóm (nặng / vừa / nhẹ / xưng hô / accuracy / độ chính xác / thành ngữ)

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
for p in phase-06-deep-learning phase-07-llm phase-08-production; do uv run python tools/validate.py --path curriculum/$p; done
grep -rnE "(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) " curriculum/phase-0[678]* --include=*.vi.md | grep -v "người ta"
grep -rn "độ chính xác" curriculum/phase-0[678]*
git diff --stat
git diff --name-only | grep -E "\.en\.md$|\.py$|\.out$" || echo "no en/py/out changes"
```
Phase 6 có bài `runner: local`. Nếu validate cần runner hoặc torch mà không có, ghi lỗi nguyên văn vào report; đừng sửa gì khác để né.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Văn VI: tự nhiên như giáo viên giỏi giảng, xưng "bạn", thuật ngữ giữ tiếng Anh (lần đầu có gloss), accuracy = "tỉ lệ đoán đúng", precision = "độ chuẩn khi báo dương", recall = "độ nhạy, tức tỉ lệ bắt được".
- Sửa YAML cẩn thận: giữ nguyên quote và indent, chạy validate sau mỗi file YAML.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: 28 file chỉ .vi.md/YAML, phần không phải vi: của YAML giống HEAD, grep ta/chúng ta 0, độ chính xác còn 6 chỗ đều là precision số thực, validate phase 6–8 0 lỗi, comment output không lệch mới, typecheck + build; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
