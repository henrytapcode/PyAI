# M4 bước 20b (nửa A): sửa p7-01..p7-05 theo review

## Mục tiêu
Sửa các lỗi reviewer tìm ra trong 5 bài đầu phase 7: p7-01-llm-api, p7-02-structured-output, p7-03-embeddings, p7-04-vector-db, p7-05-rag (danh sách tóm tắt ở `tasks/m4-p7-review.md`, mục "Nửa A"). Chỉ sửa nội dung, không thêm bài mới.
- Mọi sửa đổi làm ở cả EN và VI, giữ parity: code block giống nhau trừ `#` comment, text fence giống hệt, mermaid cùng số dòng, callout cùng thứ tự.
- Mọi số in ra phải là số chạy thật.

## File được phép sửa/tạo
- Mọi file trong `curriculum/phase-07-llm/p7-01-llm-api/**`, `p7-02-structured-output/**`, `p7-03-embeddings/**`, `p7-04-vector-db/**`, `p7-05-rag/**`.
  Được đổi tên thư mục exercise nếu đổi đề (cập nhật `exercise.yaml` id/title cho khớp; id giữ nguyên dạng `p7-0N-ex0M`).
- `curriculum/glossary.yaml`: chỉ **thêm** term, không sửa hay xóa dòng có sẵn.
- `tasks/m4-p7-review-fixes-a.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, p7-06..p7-10, các phase khác, `docs/**`.
- Không sửa `pyai_llm`. Nếu cần hành vi khác của FakeLLM, ghi vào report, không tự sửa.

## Việc cần làm

### B1. Solution không được chép code trong bài học (blocker)
Ba bài tập dưới đây phải đổi yêu cầu. Lời giải mới không được trùng (theo AST, bỏ docstring) với bất kỳ hàm hay class nào trong `lesson.*.md` và `examples/`.

1. **p7-05 ex01 → `chunk_paragraphs(text: str, max_words: int) -> list[str]`** (kind giữ `fill` hoặc đổi sang `code`, tùy bạn; lesson p7-05 vẫn còn bài `fill`/`debug` nào thì Track A mới đạt, nên nếu ex01 đổi sang `code` thì ex02 phải có ít nhất một phần `fill`/`debug`. Cách đơn giản nhất: giữ ex01 là `fill`.)
   - Tách đoạn theo dòng trống: `text.split("\n\n")`, `strip()` từng đoạn, bỏ đoạn rỗng.
   - Gộp tham lam các đoạn liền nhau vào cùng chunk khi tổng số từ (theo `split()`) ≤ `max_words`. Các đoạn trong một chunk nối bằng `"\n\n"`.
   - Một đoạn dài hơn `max_words` đứng riêng thành một chunk, không cắt.
   - `max_words <= 0` thì `raise ValueError`. Text rỗng hoặc toàn khoảng trắng thì trả `[]`.
   - Có 4–6 test, trong đó có: gộp đúng; đoạn quá dài đứng riêng; ranh giới đúng bằng `max_words` vẫn gộp; text rỗng; `ValueError`.
   - Trong lesson §1 (chỗ nói chunking), thêm 1–2 câu: chunk theo đoạn giữ trọn ý của tác giả, đổi lại kích thước chunk không đều. Bài tập sẽ cho bạn tự làm.
   - Cập nhật prompt, hint (3 tầng đúng luật ở B2), alternatives (nếu kind `code`), quiz/flashcard nào đang nhắc ex01.
2. **p7-04 ex02 `MiniStore`**: giữ tên class, thêm yêu cầu mà lesson không có:
   - `add(...)` với `doc_id` đã tồn tại thì **thay thế** bản cũ (upsert), không tạo bản trùng, `len` không đổi.
   - `search(..., where=...)`: giá trị trong `where` được phép là list, nghĩa là "một trong các giá trị này" (`{"lang": ["en", "vi"]}`). Giá trị thường thì so bằng `==`. Key không có trong metadata thì không khớp (kể cả khi giá trị là `None`, xem m6).
   - Thêm 3–4 test cho upsert và `where` dạng list. Starter vẫn fail mọi test.
   - Lesson §2/§4 giữ nguyên `VectorStore`. Thêm 1 câu ở cuối §4: store thật hỗ trợ upsert và lọc kiểu "in", bài tập sẽ cho bạn tự làm.
3. **p7-02 ex01 `check_reply`** (fill): đề mới thêm luật `enum`. Schema có thể có `"enum": [...]` ở một field; giá trị không nằm trong list thì thêm lỗi `"<field>: must be one of [...]"` (chốt định dạng chính xác trong prompt và test).
   - Các blank (`___`) phải nằm ở phần **mới** (luật enum, và phần thu thập lỗi theo đúng thứ tự). Không được khoét blank vào đúng mấy dòng mà lesson đã in.
   - Thêm 2 test cho enum. Starter vẫn fail.

Ba bài nhẹ hơn (p7-01 ex02, p7-02 ex02, p7-05 ex02) **giữ đề**, chỉ sửa hint theo B2.

### B2. Hint leo thang đúng luật (blocker)
Áp dụng cho **mọi** exercise trong 5 bài, ở cả en và vi:
- Hint 1: ý tưởng + mục trong bài + kết quả cho một input cụ thể.
- Hint 2: các bước bằng lời, dạng danh sách đánh số. **Không** có biểu thức Python hoàn chỉnh. Được nhắc tên hàm/method trong backtick (`np.argsort`), nhưng không viết nguyên lời gọi kèm tham số.
- Hint 3: skeleton trong python fence, có khung control flow và tên biến, bỏ trống (`...`) **phần lõi** (1–2 chỗ). Ví dụ: phần chấm điểm + chọn top-k (p7-03 ex02), phần dựng messages và tách citation (p7-05 ex02), thân `add` / `search` (p7-04 ex02), vòng retry (p7-01 ex02), vòng feedback (p7-02 ex02).
- Với bài `fill`: hint 3 chỉ gợi ý **blank khó nhất**, không điền các blank còn lại.
- Ghép hint 2 + hint 3 không được ra nguyên solution.
- m11: hint 1 của p7-05 ex01 phải gọi đúng tên hàm mới. Hint 3 của p7-01 ex02 phải `raise ValueError` (khớp solution).

### M1. Regex trong p7-05
Ngay chỗ `re.findall(r"\[(\d+)\]", ...)` xuất hiện lần đầu trong lesson, thêm một đoạn ngắn (2–3 câu) kèm một khối python nhỏ có output:
- `\[` nghĩa là dấu `[` thật;
- `(\d+)` bắt một hay nhiều chữ số;
- `findall` trả list **chuỗi**, nên cần `int(...)`.

### M2. `__post_init__`
Ở lần dùng đầu (p7-01 `examples/02_chat_session.py` và `.en/.vi.md` tương ứng, rồi p7-02 lesson quanh l.158), thêm một câu: dataclass tự gọi `__post_init__` ngay sau `__init__` được sinh tự động, đây là chỗ đặt kiểm tra dữ liệu. Thêm term `__post_init__` vào glossary nếu chưa có.

### M3. Overlap ở p7-05
- l.28: thay "never sliced in half" bằng ý: overlap làm giảm khả năng một câu bị cắt đôi; chỉ cụm dài tối đa `overlap + 1` từ mới chắc chắn nằm trọn trong một chunk.
- Sửa câu "Fix" ở l.327 cho khớp.
- Sửa bản VI tương ứng.

### M4. p7-01 ex02: test làm tròn
Thêm test có giá trị chưa làm tròn dài hơn 6 chữ số, ví dụ `Usage(333, 777, 1110)` với giá trong test. Tính kỳ vọng bằng `round(..., 6)` rồi viết hằng số vào test. Kiểm bằng mutant: bỏ `round` thì test phải fail.

### M5. Distractor MCQ
Viết lại distractor vô lý thành hiểu nhầm có thật:
- p7-03: q01, q03
- p7-04: q01, q07, q09, q10
- p7-05: q08, q14

Giữ `answer`, id, số phương án. Giữ luật độ dài (script ở dưới phải in `violations: 0` và `longest-unique` ≤ 1/3 mỗi file).

### Minor
1. m1: Sửa mọi tham chiếu số dòng trong `examples/*.en.md` / `.vi.md` của 5 bài cho đúng file `.py` hiện tại. Đếm bằng script, không đoán.
2. m2: p7-01 lesson (l.241-242, en + vi): đổi thứ tự, đưa `echo '.env' >> .gitignore` lên **trước** dòng ghi key.
3. m3: p7-01 TIP quanh l.126: thêm ý "với API thật, `temperature=0` chỉ **gần như** tất định". Explanation của quiz q09 khớp theo.
4. m4: p7-02:
   - §1–2: thêm NOTE rằng `response_format={"type": "json", "schema": ...}` là dạng của FakeLLM; provider thật đặt tên trường khác (ví dụ `json_schema`, `strict`), cần đọc docs của provider.
   - §5: thêm 1 câu rằng Pydantic mặc định (lax mode) đổi `"1042"` thành `1042`, còn `validate()` tự viết thì từ chối; muốn chặt thì dùng `strict=True`.
5. m5: p7-02 ex02: bỏ luật "raise nếu parsed value không phải dict" (prompt, solution, alternatives, test nếu có), hoặc ghi rõ đó là kiểm tra phòng xa. Chọn cách bỏ nếu không có test nào phụ thuộc.
6. m6: p7-04 lesson §3 (l.163, l.208) và mọi hint: dùng `key in meta and meta[key] == val` thay cho `meta.get(key) == val`.
7. m7: p7-04 NOTE quanh l.393: đổi "pre-filter" thành "filtered search", kèm 1 câu rằng có hệ lọc trước, có hệ lọc sau khi tìm.
8. m8: p7-03 sau bảng cosine (l.78-82): thêm 1 câu: với model thật, hai văn bản không liên quan vẫn thường có cosine > 0 rõ rệt; ngưỡng phải đo lại cho từng model.
9. m9: p7-05 quanh l.331: sửa lời văn cho khớp code (`range` với step 0 thì raise `ValueError`, không treo), hoặc đổi code cho khớp lời văn. Output là số chạy thật.
10. m10: p7-05 §4: thêm 1 câu nối: "Ở đây hits là dict cho gọn; trong p7-04 bạn đã dùng `Hit` với `.text`, ý tưởng như nhau." Nếu `build_messages` ở p7-05 trùng tên với p7-01 mà khác chữ ký, đổi tên ở p7-05 thành `build_rag_messages` (cập nhật mọi chỗ trong p7-05).
11. m12: VI hint:
    - p7-04 ex01: "đúng/sai" → `True`/`False`.
    - p7-02 ex01: "nhận giá trị kiểu `bool`".
    - p7-03 ex01: "trả về `0.0`".
12. m13: p7-04 lỗi thường gặp 1: gọi `store.add` thật (dùng `VectorStore` định nghĩa lại ngắn hoặc trích từ §2) để thấy lỗi, thay vì `raise` rồi `except` ngay trong cùng khối. Khối phải tự chạy được.

## Tiêu chí hoàn thành (checklist)
- [ ] B1: 3 đề mới; lời giải không trùng lesson/examples (AST); starter fail mọi test; solution + alternatives pass
- [ ] B2: mọi hint 3 tầng đúng luật ở 10 exercise
- [ ] M1–M5 xong; mutant M4 bị bắt
- [ ] m1–m13 xong (m11 nằm trong B2)
- [ ] Script MCQ: `violations: 0`, longest-unique ≤ 1/3 mỗi file
- [ ] Validate 5 bài 0 lỗi; pytest phase 7 xanh; ruff sạch; mọi khối python mới chạy với `-W error`, stderr rỗng
- [ ] `git diff --numstat curriculum/glossary.yaml` có 0 dòng xóa
- [ ] Không file nào ngoài phạm vi bị sửa

## Lệnh kiểm tra
```bash
for d in p7-01-llm-api p7-02-structured-output p7-03-embeddings p7-04-vector-db p7-05-rag; do uv run python tools/validate.py --path curriculum/phase-07-llm/$d; done
uv run python -m pytest curriculum/phase-07-llm -q -p no:warnings
uv run ruff check
git diff --numstat curriculum/glossary.yaml
```
Kiểm độ dài MCQ (phải in `violations: 0`; `longest-unique` mỗi file ≤ 1/3 số MCQ):
```bash
uv run python -c "
import yaml,glob
bad=0
for f in sorted(glob.glob('curriculum/phase-07-llm/p7-0[1-5]*/quiz.yaml')):
    n=lu=0
    for q in yaml.safe_load(open(f,encoding='utf-8'))['questions']:
        if q['type']!='mcq': continue
        n+=1
        for lang in ('en','vi'):
            o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
            d=[l for i,l in enumerate(L) if i!=a]
            if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
            if lang=='en' and L[a]==max(L) and L.count(L[a])==1: lu+=1
    print(f, 'mcq', n, 'longest-unique', lu)
print('violations:',bad)
"
```
Starter phải fail: với mỗi exercise bị sửa, copy `starter.py` thành `exercise.py` trong thư mục tạm cùng `test_exercise.py`, chạy pytest, báo số test fail/tổng. Làm tương tự cho mutant ở M4.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Code phase 7 gọi LLM chỉ qua `pyai_llm` (xem CONTENT_GUIDE, mục "Fake LLM client").
- Test chỉ dùng tập con được phép (assert, pytest.raises/approx/mark.parametrize/fail, fixture trong file, capsys, tmp_path, caplog, monkeypatch).
- Quiz `output`/`fill`/`parsons` bị sửa phải chạy đúng (validate sẽ chạy).

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate 5 bài 0 lỗi, pytest phase 7 172 pass, ruff curriculum sạch, typecheck + build 72 trang, validate toàn bộ 0 lỗi trên 49 bài; trong app: khối regex p7-05 chạy đúng, ex01 chunk_paragraphs starter 0/8, solution 8/8; đã commit `965d73f`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
