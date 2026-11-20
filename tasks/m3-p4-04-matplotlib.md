# M3 bước 5: bài p4-04 Plotting với Matplotlib

## Mục tiêu
Viết bài `p4-04-matplotlib` đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
Người học đã xong `p4-01-numpy`, `p4-02-pandas`, `p4-03-cleaning`; **chưa biết matplotlib**.
App đã hiển thị biểu đồ: khi bấm Run, mọi figure đang mở được vẽ thành ảnh trong ô Output (bước M3-1). Local: `MPLBACKEND=Agg`, `.out` chỉ so **stdout**, ảnh không bị so.
Bài mẫu về giọng văn và hình dạng: `curriculum/phase-04-data/p4-03-cleaning/` (đã duyệt).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-04-matplotlib/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (figure, axes, legend, scatter plot, bar chart, line chart; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p4 khác, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Quy tắc output (bắt buộc)
- App chạy Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên, không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`.
- Không in list/tuple/dict chứa numpy scalar (numpy 2 in `np.float64(...)`, `np.int64(...)`): dùng `.tolist()`, `float()`, `int()`.
- DataFrame in ra tối đa 4 cột, dòng dưới 60 ký tự.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật (boss chạy từng khối để đối chiếu).
- **Biểu đồ không có trong stdout**: mọi example vẽ biểu đồ phải **in thêm** một dòng tóm tắt bằng chữ (vd mốc tốt nhất, tổng theo nhóm) để `.out` có nội dung. Trong lesson, sau `plt.show()` ghi comment kiểu `# (shows a line chart: ...)` / VI `# (hiện biểu đồ đường: ...)` mô tả biểu đồ sẽ thấy.
- Chuỗi trong code (title, label) giữ tiếng Anh như mọi code khác.
- Local matplotlib là 3.9.2, app là 3.8.4: chỉ dùng API có ở cả hai (không dùng tính năng mới của 3.9).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): một biểu đồ cho thấy ngay loss đang giảm hay mô hình nào rẻ nhất, điều mà bảng số khó thấy. Matplotlib là thư viện vẽ chuẩn của Python; pandas cũng vẽ qua nó. Nhắc: lần Run đầu tiên app tải matplotlib nên mất vài giây.

1. **Biểu đồ đầu tiên**: `import matplotlib.pyplot as plt`, `fig, ax = plt.subplots()`, `ax.plot(x, y)`, `plt.show()`. Dạy **kiểu hướng đối tượng** (`fig, ax`) làm chính; một câu nói `plt.plot(...)` là lối tắt. **Picture in text** (fence `text`): figure là tấm canvas, axes là một biểu đồ bên trong, có trục x/y, tiêu đề, chú thích.
2. **Nhãn và chú thích**: `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `label=` + `ax.legend()`, `marker="o"`, `ax.grid(True)`. Ví dụ: train loss và validation loss qua 6 epoch. Kèm **bảng dữ liệu** `| epoch | train_loss | val_loss |` và một câu đọc biểu đồ (val loss bắt đầu tăng = dấu hiệu overfitting, nhắc sẽ học ở phase 5).
3. **Biểu đồ cột**: `ax.bar(names, values)`, sắp xếp dữ liệu trước khi vẽ; `ax.barh` cho nhãn dài.
4. **Scatter**: `ax.scatter(x, y)` cho số token và độ trễ; một câu: điểm đi lên theo đường chéo = hai đại lượng tăng cùng nhau.
5. **Vẽ từ DataFrame**: `df.plot(x="epoch", y=["train_loss", "val_loss"], ax=ax)`, và `df.groupby("model")["cost"].sum().sort_values().plot(kind="bar", ax=ax)`. Đây là section mời bấm **Visualize** ở một khối nhỏ chuẩn bị dữ liệu (groupby + sort) trước khi vẽ.
6. **Chọn loại biểu đồ**: **mermaid** `flowchart TD` (tối đa 8 node, mọi nhãn trong ngoặc kép) theo câu hỏi: so sánh nhóm? → bar; thay đổi theo thời gian/epoch? → line; quan hệ giữa hai số? → scatter. **Bảng so sánh** `| question | chart | matplotlib call |`.
7. **Nhiều biểu đồ cạnh nhau**: `fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))`, `fig.tight_layout()`.
8. **Lỗi thường gặp** (3–4, chạy thật để lấy đúng thông báo):
   - `ax.title("Loss")` → `TypeError: 'Text' object is not callable`; dùng `ax.set_title(...)`.
   - Gọi `ax.legend()` mà không đặt `label=` → cảnh báo "No artists with labels found to put in legend", chú thích rỗng.
   - Vẽ đường với x chưa sắp xếp → đường zigzag; sắp xếp trước.
   - Trộn `plt.xlabel(...)` với nhiều `ax` → nhãn rơi vào biểu đồ cuối cùng; dùng `ax.set_xlabel`.
9. **Recap / Tóm tắt**.

Thời lượng 10–12 phút. `review_by: "2027-11-01"`. `further_reading`: Matplotlib "Quick start guide" và trang "Plotting" trong pandas user guide (URL chính thức).

## Examples (3)
- `01_loss_curve`: train/val loss qua các epoch, vẽ 2 đường có legend; in epoch có val loss thấp nhất.
- `02_cost_by_model`: DataFrame chi phí API, groupby model, biểu đồ cột sắp xếp giảm dần; in tổng chi phí từng model (dạng `model: 1.23`).
- `03_latency_scatter`: số token và độ trễ của 8 request, scatter có nhãn trục; in hệ số tương quan `round(float(np.corrcoef(x, y)[0, 1]), 2)`.

## Exercises (2)
Mọi hàm vẽ trong bài tập **trả về `(fig, ax)`** để test đọc được thuộc tính, và **không gọi `plt.show()`** bên trong hàm.
- `ex01-loss-chart` (`kind: fill`): `plot_loss(epochs: list[int], losses: list[float]) -> tuple`: tạo `fig, ax`, vẽ đường có `label="loss"` và `marker="o"`, đặt title `"Training loss"`, xlabel `"epoch"`, ylabel `"loss"`, gọi `ax.legend()`. Các ô `___` trong thân hàm. Test đọc: `ax.get_title()`, `ax.get_xlabel()`, `ax.get_ylabel()`, `len(ax.lines) == 1`, `ax.lines[0].get_xdata()` / `get_ydata()` (so bằng `list(...)` + `pytest.approx`), chữ trong legend (`[t.get_text() for t in ax.get_legend().get_texts()]`).
- `ex02-cost-bar-chart` (`kind: code`): `cost_bar_chart(df: pd.DataFrame) -> tuple`: df có cột `model`, `cost`; tổng `cost` theo `model`, sắp xếp **giảm dần**, vẽ `ax.bar`, title `"Cost by model"`, ylabel `"cost (USD)"`. Test: chiều cao cột `[float(p.get_height()) for p in ax.patches]` (dùng `pytest.approx`), nhãn trục x `[t.get_text() for t in ax.get_xticklabels()]` theo đúng thứ tự giảm dần, title/ylabel, model chỉ xuất hiện một lần, không sửa df. 4–6 test. Có `alternatives/01_pandas_plot.py` dùng `Series.plot(kind="bar", ax=ax)` + `.md` so sánh (lưu ý: nếu cách pandas làm nhãn trục khác, ví dụ xlabel tự đặt là `"model"`, test không được kiểm `xlabel`; cả hai cách phải qua cùng bộ test).
- Mỗi test tự đóng figure sau khi kiểm (`plt.close(fig)`) để không rò bộ nhớ khi chạy nhiều test.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `plotting` (chính), có thể thêm `pandas`.
Câu `output` phải in ra chữ (vd `print(ax.get_title())`, `print(len(ax.lines))`), không dựa vào ảnh. Câu `output`/`fill`/`parsons` có matplotlib phải chạy được với backend Agg (validator đã đặt sẵn).

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 4`, `tags` gồm `plotting`, `prerequisites: [p4-02-pandas]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý trên, đủ: mermaid, picture in text, bảng dữ liệu, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output" ở trên.
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; gợi ý tầng 3 chừa ít nhất 2 chỗ `...`.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh.
8. [ ] Chạy `uv run python tools/build_content.py` (an toàn khi dev server đang chạy) để app thấy bài mới. Nếu có công cụ trình duyệt: mở `http://localhost:3000/lesson/p4-04-matplotlib/`, Run một khối có biểu đồ và ghi kết quả; không có thì ghi rõ trong report (boss sẽ tự kiểm).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-04-matplotlib
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
grep -rnE "astype\(int\)|dtype=int\b|\.info\(" curriculum/phase-04-data/p4-04-matplotlib
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0 (không treo); ruff sạch; grep rỗng; file mới chỉ trong `p4-04-matplotlib/` (và `glossary.yaml`).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, rồi `curriculum/phase-04-data/p4-03-cleaning/`.
- Chạy pytest local nếu cần đặt `MPLBACKEND=Agg` (validator và browser runner đã tự đặt). Nếu pytest mở cửa sổ hoặc treo, đặt biến môi trường khi chạy lệnh, **không** sửa `conftest.py` hay `tools/`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 2: vòng 1 lộ lỗi treo validate do tracer chưa đặt Agg; boss tự kiểm tra trong app; chờ user duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Nội dung bài chưa bị chê; lỗi nằm ở hạ tầng (sót từ bước M3-1), cần sửa để cổng chạy được **không cần** đặt `MPLBACKEND` bằng tay:
- `uv run python tools/validate.py` (không biến môi trường) **treo vô hạn**: `check_examples` (validate.py dòng ~231) gọi tracer `tools/pyrunner/tracer.py` ngay trong tiến trình validate; tracer không đặt backend Agg nên `plt.show()` ở dòng 16 của example mở cửa sổ Tk và chờ (`tkinter mainloop`). Stack đo được: `validate.py:231 check_examples → tracer.py:116 trace → <main> line 16 → pyplot.show → _backend_tk start_main_loop`.
- Report vòng trước ghi pytest/validate xanh "với `MPLBACKEND=Agg`": lần sau phải chạy đúng lệnh trong spec, không thêm biến môi trường.

Cho phép sửa thêm (chỉ đúng chỗ này):
- `tools/validate.py`: ngay sau các dòng import ở đầu file, đặt `os.environ.setdefault("MPLBACKEND", "Agg")` kèm một comment ngắn (tracer và browser runner chạy trong tiến trình validate). Giữ nguyên `MPLBACKEND="Agg"` trong `run_python`.
- `curriculum/conftest.py`: thêm `os.environ.setdefault("MPLBACKEND", "Agg")` ở cấp module (sau `import os`) kèm comment, để `uv run python -m pytest curriculum` không bao giờ dùng backend có cửa sổ.
Không sửa `tracer.py`, `runner.py` hay file nào khác trong `tools/`.

Kiểm tra lại (PowerShell mới, **không** đặt `MPLBACKEND`):
```
uv run python tools/validate.py
uv run python -m pytest curriculum
```
Cả hai phải xong (validate trước đây khoảng 1–2 phút) và xanh. Ghi thời gian chạy vào report.
