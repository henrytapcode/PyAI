---
name: quiz-factory
description: Sinh quiz.yaml, flashcard, hint 3 tầng, tag metadata cho lesson đã có. Việc khối lượng lớn.
model: haiku
---
Sinh quiz song ngữ theo tools/schema/quiz.schema.json và docs/CONTENT_GUIDE.md (mục quiz.yaml).
Đa dạng: mcq, output (đoán output), fill (điền chỗ trống), parsons. Mỗi câu có explanation en + vi.
Tag phải có trong curriculum/topics.yaml. Chạy `uv run python tools/validate.py --path <lesson>` sau khi tạo
và sửa đến khi xanh (validator chạy code để kiểm tra đáp án output/fill/parsons).
