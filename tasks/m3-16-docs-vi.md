# M3 bước 16: cập nhật tài liệu dự án + đọc mẫu bản VI phase 4–5

## Mục tiêu
Hai việc độc lập:
- **A. Tài liệu:** cập nhật `CLAUDE.md`, `docs/DESIGN.md` và `docs/CONTENT_GUIDE.md` cho đúng trạng thái sau M3 (phase 4–5 và mock exam xong), và ghi lại các quy tắc học được trong M3 để M4 không lặp lỗi.
- **B. Đọc mẫu bản VI:** đọc 3 bài (khoảng 25% phase 4–5) như một giáo viên người Việt rồi sửa chỗ gượng, dịch sát chữ hoặc sai nghĩa. Các bài: `p4-03-cleaning`, `p5-02-supervised`, `p5-04-evaluation`.

## File được phép sửa
- `CLAUDE.md`, `docs/DESIGN.md`, `docs/CONTENT_GUIDE.md`
- Ba file `lesson.vi.md`: `curriculum/phase-04-data/p4-03-cleaning/`, `curriculum/phase-05-ml/p5-02-supervised/`, `curriculum/phase-05-ml/p5-04-evaluation/`
- Các file `examples/*.vi.md` của ba bài đó

## Không được đụng
- Mọi file `.en.md`, `.py`, `.yaml` (kể cả `quiz.yaml`, `glossary.yaml`), `tools/`, `apps/`. Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## A. Tài liệu (nội dung boss chốt)
1. `CLAUDE.md`, mục "Quy trình", dòng "Hiện tại: …":
   - Ghi M3 đã xong: phase 4 (6 bài và phase test), phase 5 (5 bài và phase test), cả hai qua reviewer; mock exam `mock-data-ml`; Visualize hiện bảng.
   - Ghi bước kế tiếp là M4 (phase 6–8, runner cục bộ).
   - Bỏ phần nói M2 và redesign đang làm. Chỉ giữ một câu ngắn rằng theme Dose đã merge.
   - Thêm một gạch đầu dòng: "Chạy pytest bằng `uv run python -m pytest` (không dùng `uv run pytest`)".
   - Giữ file dưới khoảng 60 dòng.
2. `docs/DESIGN.md`:
   - §5, dòng Chạy Python: ghi Pyodide 0.29.5 có sẵn numpy, pandas, matplotlib, scikit-learn, scipy, sqlite3. Ghi thêm: môi trường local ghim phiên bản (vd `scipy==1.14.1`) để output khớp với app.
   - §5: thêm một câu về **Visualize**. Đây là tracer `tools/pyrunner/tracer.py` chạy từng bước, giới hạn 600 bước, hiện DataFrame/Series/mảng 2D thành bảng 8×6.
   - §10: ghi "M3 xong (2026-11-14)" ở dòng M3.
   - Không viết lại các phần khác.
3. `docs/CONTENT_GUIDE.md`: thêm mục mới `## Data & ML code (phase 4+)` trước `## Quality gate`, viết bằng tiếng Anh như phần còn lại, mỗi ý một gạch đầu dòng ngắn. Nội dung lấy từ đầu `tasks/M3-PLAN.md` và các spec `tasks/m3-p5-*.md`:
   - Pyodide là wasm32: NumPy int mặc định là `int32`. Không in dtype số nguyên; dùng `"int64"`, không dùng `astype(int)`; không dùng `df.info()`.
   - In giá trị bằng `.tolist()` / `round(float(x), 3)`, không in numpy scalar (numpy 2 in ra `np.float64(...)`).
   - DataFrame in ra tối đa 4 cột, mỗi dòng dưới 60 ký tự.
   - Không được có warning nào. Kiểm bằng `-W error`.
   - Ngẫu nhiên chỉ qua `np.random.default_rng(seed)` và `random_state`. Không dùng `fetch_*` hay mạng. matplotlib dùng backend Agg, không gọi `plt.show()` trong code chấm.
   - SQLite chỉ dùng `":memory:"`. Mọi `SELECT` trả nhiều dòng phải có `ORDER BY`.
   - Khối nào mời bấm Visualize thì phải ngắn (dưới 600 bước).
   - "Test set is used once": chọn mô hình, hyperparameter và threshold bằng CV hoặc tập validation tách từ train. Trước khi dạy CV, gọi một lần chia là "a first look".
   - `zero_division`: trên sklearn 1.7 chỉ precision cảnh báo khi TP+FP=0.
   - Thuật ngữ VI: accuracy = "tỉ lệ đoán đúng"; precision = "độ chuẩn khi báo dương"; recall = "độ nhạy, tức tỉ lệ bắt được".
   - Câu mcq trong bài thi: 4 lựa chọn dài gần bằng nhau, không nhét lý do vào lựa chọn đúng.

## B. Đọc mẫu VI
Đọc từng bài (lesson.vi.md và examples/*.vi.md), so với bản EN để hiểu ý. Sửa:
- câu dịch sát chữ, trật tự tiếng Anh, từ gượng (vd "bảng vết", "mặt phẳng" dùng sai, "lệch chuẩn");
- câu sai nghĩa so với EN;
- thuật ngữ lệch quy ước ở mục A.3 hoặc không thống nhất trong cùng bài;
- lần đầu dùng thuật ngữ mà thiếu giải nghĩa: "**thuật ngữ tiếng Việt** (English term)" hoặc giữ tiếng Anh kèm giải nghĩa.

Giữ nguyên tuyệt đối (validator so EN/VI):
- mọi khối code (chỉ dịch được comment `#`);
- khối ```` ```text ````;
- số dòng của khối mermaid;
- thứ tự và loại callout;
- số heading, bảng (số dòng, số cột), link.

Không viết lại cả đoạn khi chỉ cần sửa vài chữ. Không đổi ý sư phạm. Giọng văn thân thiện, gọi người đọc là "bạn".

## Tiêu chí hoàn thành (checklist)
1. [ ] A.1–A.3 đúng nội dung trên, không sửa phần khác của tài liệu.
2. [ ] B: report có bảng `file | trước | sau | lý do` cho **mọi** chỗ sửa (dự kiến 10–30 chỗ mỗi bài; nếu bài nào gần như không cần sửa thì nói rõ).
3. [ ] Report ghi 3–5 lỗi văn phong VI lặp lại nhiều nhất, để boss đưa vào quy tắc sau này.
4. [ ] Lệnh kiểm tra xanh; `git status` chỉ có các file trong danh sách được phép. (`CLAUDE.md` và `docs/` bị gitignore nên không hiện trong `git status`, đó là bình thường.)

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-03-cleaning
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-02-supervised
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-04-evaluation
uv run python tools/validate.py
grep -nE "độ chính xác|độ phủ|bảng vết|chuyển ca trực|hậu kiểm" curriculum/phase-04-data/p4-03-cleaning/*.vi.md curriculum/phase-04-data/p4-03-cleaning/examples/*.vi.md curriculum/phase-05-ml/p5-02-supervised/*.vi.md curriculum/phase-05-ml/p5-02-supervised/examples/*.vi.md curriculum/phase-05-ml/p5-04-evaluation/*.vi.md curriculum/phase-05-ml/p5-04-evaluation/examples/*.vi.md
git status --short
```
Mong đợi: validate 0 lỗi; grep rỗng.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` mục Vietnamese trước khi sửa.
- Dùng `uv run python -m pytest` nếu cần chạy test, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss so diff CLAUDE.md/docs với bản lưu, đọc từng chỗ sửa VI, validate 3 bài xanh; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
- Boss lưu bản trước của CLAUDE.md và docs/ (gitignore) trong scratchpad để so diff
