# M4 bước 20b (nửa B): sửa p7-06..p7-10 theo review

## Mục tiêu
Sửa các lỗi reviewer tìm ra trong 5 bài cuối phase 7: p7-06-tool-use, p7-07-agents, p7-08-evals, p7-09-mini-project-rag, p7-10-mini-project-agent. Bản tóm tắt nằm ở `tasks/m4-p7-review.md`, mục "Nửa B". Chỉ sửa nội dung, không thêm bài mới.

Mọi sửa đổi làm ở cả EN và VI, giữ parity:
- code block giống nhau, chỉ khác `#` comment;
- text fence giống hệt;
- mermaid cùng số dòng;
- callout cùng thứ tự.

Mọi số in ra phải là số chạy thật.

## File được phép sửa/tạo
- Mọi file trong `curriculum/phase-07-llm/p7-06-tool-use/**`, `p7-07-agents/**`, `p7-08-evals/**`, `p7-09-mini-project-rag/**`, `p7-10-mini-project-agent/**`.
- `curriculum/glossary.yaml`: chỉ **thêm** term, không sửa hay xóa dòng có sẵn.
- `tasks/m4-p7-review-fixes-b.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, p7-01..p7-05, các phase khác, `docs/**`.
- Không sửa `pyai_llm`. Nếu cần FakeLLM chạy khác đi, ghi vào report, không tự sửa.

## Việc cần làm

### B1. p7-06 §6: guard để model tự cấp quyền (blocker)
Ở `lesson.en.md` (khoảng l.315-347) và `lesson.vi.md`, `issue_refund(**args)` cho phép args do model đưa vào tự đặt `confirmed=True` và nâng `max_amount`. Sửa giống `examples/03_refund_guard.py`:
- `issue_refund(order_id, amount)` chỉ nhận hai tham số.
- Hạn mức là hằng số `MAX_AUTO_REFUND` trong code.
- Cờ xác nhận là tham số của guard: `run_guarded(tool_name, args, user_confirmed: bool)`. Giá trị này lấy từ trạng thái app, không lấy từ `args`.
- Guard chỉ truyền `order_id` và `amount` vào tool. Key lạ trong `args` (như `confirmed`, `max_amount`) thì bị bỏ qua, hoặc trả `"blocked: unexpected argument ..."`; chọn một cách và in ra để minh họa.
- Thêm một dòng demo: model cố gửi `{"confirmed": True, "max_amount": 1000.0, ...}` và vẫn bị chặn.
- Câu "Notice" sau code chỉ ra đúng chỗ này.
- Mọi `# output` là số chạy thật. Quiz/flashcard nào nhắc code cũ thì sửa cho khớp.

### M1. p7-10 ex02: test phải bắt được history
Thêm vào `test_exercise.py` một spy client ghi lại `messages` của mỗi lần `chat` (xem cách p7-07 ex02 làm). Test assert rằng sau lần gọi tool đầu, lần `chat` thứ hai nhận:
- `messages[1]["role"] == "assistant"` và có `tool_calls`;
- `messages[2]["role"] == "tool"` với `tool_call_id` khớp id của tool call.

Kiểm bằng mutant: bỏ hai lệnh append thì test phải fail.

### M2. p7-10: tách `rejected` khỏi `needs_approval`
- `approve` là `None` (không có ai duyệt): `stopped_reason = "needs_approval"`, như p7-07 §6.
- `approve(...)` trả `False` (policy từ chối): `stopped_reason = "rejected"`. Tool không chạy.

Cập nhật mọi chỗ liên quan:
- lesson (code, bảng, mermaid nếu có, các dòng output, phần giải thích, kể cả l.305, 370, 414);
- scenario `refund_rejected` và mọi scenario khác bị ảnh hưởng;
- kết quả v1/v2 in ra: chạy lại, ghi số thật;
- ex02: prompt (rule 4), starter docstring, solution, alternatives, test (thêm 1 test cho `rejected`), hint;
- quiz/flashcard có nhắc tới.

### M3. p7-08 ex01: không chép `hit_rate` của lesson
Đổi đề thành `hit_rates(results: list[dict], ks: list[int]) -> dict[int, float]`: trả hit rate cho từng `k` trong `ks`, làm tròn 3 chữ số. Giữ cách xử lý `results` rỗng như solution hiện tại.
- Có `k <= 0` trong `ks` thì `raise ValueError` (gộp luôn m2).
- Giữ kind `fill`. Các blank phải nằm ở phần mới (vòng qua `ks`, kiểm `k`), không đặt vào mấy dòng mà lesson §3 đã in.
- Thêm test cho nhiều `k`, `k=0` và `k=-1`. Starter fail mọi test.
- Cập nhật prompt, hint, quiz nếu có nhắc.

p7-06 ex01 (fill): chuyển các blank đang trùng nguyên dòng với `tool_schema` ở §2 sang phần lesson không in sẵn, ví dụ phần dựng `required` hay kiểu của tham số. Nếu không làm được thì thêm một yêu cầu nhỏ mới, có test. Starter vẫn fail.

### M4. Hint leo thang đúng luật
Áp dụng cho **mọi** exercise trong 5 bài, ở cả en và vi:
- **Hint 1:** ý tưởng, kèm mục trong bài và kết quả cho một input cụ thể.
- **Hint 2:** các bước bằng lời, dạng danh sách đánh số.
  - **Không** có biểu thức Python hoàn chỉnh.
  - Được nhắc tên hàm/method trong backtick, nhưng không viết nguyên lời gọi kèm tham số.
  - Bỏ `make_client(list(scenario["script"]))`, `client.chat(messages, tools=...)`, `toolbox.call(...)` khỏi hint 2 của p7-10 ex02; bỏ `k <= 0` ở p7-09 ex01, `schema["name"]` và `json.dumps()` ở p7-10 ex01.
- **Hint 3:** skeleton trong python fence, có khung và tên biến, bỏ trống (`...`) **phần lõi**, đúng 1–2 chỗ.
  - p7-10 ex01 hiện có 4 chỗ `...`, cần gộp lại.
  - p7-08 ex02 đang đưa khoảng 90% lời giải: để trống cả phần chấm `facts`/`faithful`, không chỉ phần citation.
- **Bài `fill`** (m12: p7-06 ex01, p7-07 ex01, p7-08 ex01): hint 3 chỉ gợi blank khó nhất, không điền các blank còn lại.
- **Kiểm tra cuối:** ghép hint 2 với hint 3 không được ra nguyên solution.

### M5. `copy.deepcopy` chưa được dạy
Ở p7-10 lesson §3 (lần dùng đầu), thêm 2–3 câu và một khối python nhỏ có output:
- copy nông (`dict(x)`, `x.copy()`) vẫn dùng chung dict/list lồng bên trong;
- `copy.deepcopy` chép cả các tầng lồng;
- ToolBox trả bản sao để code gọi bên ngoài không sửa được schema bên trong.

Thêm term `deep copy` vào glossary nếu chưa có.

### Minor
1. m1 p7-07 ex02: trong `test_three_step` (hoặc test mới), assert `json.loads(obs)["note"] == "ok"`, hoặc kiểm tương đương rằng tham số tùy chọn rỗng `""` đã bị bỏ. Kiểm bằng mutant: bỏ bước strip thì test phải fail.
2. m3 p7-09 ex01: thêm test `ValueError` khi `size`/`overlap` sai (theo đúng luật trong prompt), và test dùng spy client để kiểm rằng không gọi `embed` khi không có chunk nào.
3. m4 p7-07 §4 (khoảng l.200-203) và p7-10: thêm 1–2 câu giải thích vì sao budget được kiểm sau `chat`. Lời gọi đã tốn tiền, và vượt budget nghĩa là dừng, kể cả khi lời đáp đó là câu trả lời cuối; một số hệ chọn kiểm `final` trước. Không đổi logic, trừ khi bạn cập nhật mọi số cho khớp.
4. m5 p7-07 §2 và p7-10: thêm NOTE rằng API thật có thể trả nhiều tool call trong một lượt. Bài này chỉ xử lý `tool_calls[0]` cho gọn; p7-06 ex02 đã xử lý tất cả.
5. m6 p7-06 l.36 và l.59: mô tả FakeLLM cho đúng.
   - FakeLLM điền mọi field kiểu string mà nó trích được (không chỉ field optional).
   - FakeLLM chọn tool theo độ trùng từ với cả `name` và `description`.
   - Đọc `pyai_llm` (grep `class FakeLLM` trong `tools/`) để viết đúng.
6. m7 `p7-06/examples/03_refund_guard.en.md` / `.vi.md`:
   - `user_confirmed` do app đặt, không phải do model đề xuất.
   - Phần "Try it yourself": ghi rõ câu trả lời cuối là script, nên khi đổi thành `False` thì bot vẫn in câu "complete". Cái cần nhìn là kết quả tool (`blocked: ...`). Hoặc sửa script để câu trả lời cuối dựa vào kết quả tool.
7. m8 p7-09 §1: thêm 1 câu nối tên metric giữa hai bài:
   - `grounded` ở đây là `faithful` của p7-08 cộng thêm yêu cầu citation hợp lệ (như p7-08 ex02);
   - `refusals` / `idk` là cùng một ý.

   Nếu tên trong lesson và ex02 của p7-09 lệch nhau (`ground` / `grounded`), thống nhất về một tên.
8. m9 p7-09 l.413-418 và l.541-546: tách `x.content or "" if top_hits else "..."` thành `if`/`else` rõ ràng. Ở lần đầu dùng regex lookbehind `(?<=[.!?])\s+`, thêm 1 câu giải thích: tách sau dấu câu, giữ lại dấu câu.
9. m10 p7-08 §5: thêm 1 câu: tập dùng để chọn k ở đây đóng vai dev set; quyết định cuối phải chấm trên tập giữ kín (p7-09 sẽ làm vậy).
10. m11 VI p7-06 §3: "(5) in câu trả lời cuối" → "(5) trả về câu trả lời cuối".

## Tiêu chí hoàn thành (checklist)
- [ ] B1: model không tự cấp `confirmed`/`max_amount` được; có dòng demo
- [ ] M1: spy test; mutant bỏ append bị bắt
- [ ] M2: `rejected` tách khỏi `needs_approval`, số v1/v2 chạy lại thật
- [ ] M3: đề `hit_rates` mới; p7-06 ex01 blank không trùng lesson; lời giải không trùng lesson/examples (AST, bỏ docstring)
- [ ] M4: mọi hint 3 tầng đúng luật ở 10 exercise
- [ ] M5, m1–m11 xong; mutant m1 bị bắt
- [ ] Mọi starter fail mọi test; solution và alternatives pass
- [ ] Script MCQ: `violations: 0`, longest-unique ≤ 1/3 mỗi file
- [ ] Validate 5 bài 0 lỗi; pytest phase 7 xanh; `ruff check curriculum` sạch; mọi khối python mới chạy với `-W error`, stderr rỗng
- [ ] `git diff --numstat curriculum/glossary.yaml` có 0 dòng xóa
- [ ] Không file nào ngoài phạm vi bị sửa

## Lệnh kiểm tra
```bash
for d in p7-06-tool-use p7-07-agents p7-08-evals p7-09-mini-project-rag p7-10-mini-project-agent; do uv run python tools/validate.py --path curriculum/phase-07-llm/$d; done
uv run python -m pytest curriculum/phase-07-llm -q -p no:warnings
uv run ruff check curriculum
git diff --numstat curriculum/glossary.yaml
```
Kiểm độ dài MCQ (phải in `violations: 0`; `longest-unique` mỗi file ≤ 1/3 số MCQ):
```bash
uv run python -c "
import yaml,glob
bad=0
for f in sorted(glob.glob('curriculum/phase-07-llm/p7-0[6-9]*/quiz.yaml')+glob.glob('curriculum/phase-07-llm/p7-10*/quiz.yaml')):
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
Starter phải fail: với mỗi exercise bị sửa, copy `starter.py` thành `exercise.py` trong thư mục tạm cùng `test_exercise.py`, chạy pytest, báo số test fail/tổng. Làm tương tự với các mutant ở M1 và m1.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Code phase 7 gọi LLM chỉ qua `pyai_llm` (xem CONTENT_GUIDE, mục "Fake LLM client"). Sau tool message, FakeLLM không gọi tiếp tool khác; muốn có nhiều bước thì dùng `script=`.
- Test chỉ dùng tập con được phép: assert, pytest.raises/approx/mark.parametrize/fail, fixture trong file, capsys, tmp_path, caplog, monkeypatch.
- Quiz `output`/`fill`/`parsons` bị sửa phải chạy đúng (validate sẽ chạy).

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate 5 bài 0 lỗi, pytest phase 7 182 pass, ruff curriculum sạch, hint 3 có 1–2 chỗ trống ở cả 10 bài, typecheck + build 72 trang, validate toàn bộ 0 lỗi trên 49 bài; trong app: p7-10 ex02 starter 0/13, lời giải cũ (thiếu rejected) 12/13, lời giải mới 13/13; đã commit `1bf8ade`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
