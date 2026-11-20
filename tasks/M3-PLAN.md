# M3: phase 4–5 + mock exam Data & ML (kế hoạch, 2026-11-13)

Nguồn: `docs/DESIGN.md` §3, §10 (M3 = phase 4–5, mock exam). Template bài: `docs/CONTENT_GUIDE.md`.
Quy trình: `/delegate` (boss viết spec `tasks/<slug>.md`, Gemini làm, boss chạy lại cổng), mỗi bước một commit sau khi user duyệt.

Pyodide 0.29.5 (Python 3.13) có sẵn: numpy 2.2.5, pandas 2.3.3, matplotlib 3.8.4, scikit-learn 1.7.0, scipy 1.14.1, sqlite3.
Worker tự tải gói theo import (`loadPackagesFromImports`).

## Quy tắc output cho mọi bài phase 4–5 (đưa vào mỗi spec)
- **Pyodide là wasm32**: số nguyên mặc định của NumPy là `int32` trong app nhưng `int64` ở local (đã đo 2026-11-13). Cột số nguyên của pandas là `int64` ở cả hai. Vì vậy: không in `dtype` của mảng NumPy số nguyên; không dùng `astype(int)` / `dtype=int` (ra `int32` trong app), dùng `"int64"` tường minh; tránh phép tính số nguyên NumPy có thể vượt 2^31.
- Không in `df.info()` (dòng memory usage khác nhau giữa 32/64-bit).
- Không in list/tuple/dict chứa numpy scalar (numpy 2 in `np.float64(...)`).
- DataFrame in ra tối đa 4 cột, dòng dưới 60 ký tự (hoặc `to_string()`).
- Comment `# output` trong lesson phải khớp output thật (boss chạy từng khối để đối chiếu).

| Bước | Slug | Nội dung | Trạng thái |
|---|---|---|---|
| 1 | `m3-01-foundation` | Thư viện data/ML cho môi trường local, hiển thị biểu đồ Matplotlib trong app, syllabus chi tiết p4–p5 | `8493356` |
| 2 | `m3-p4-01-numpy` | Bài p4-01 NumPy | `67492fc` |
| 3 | `m3-p4-02-pandas` | Bài p4-02 Pandas | `b8e334d` |
| 4 | `m3-p4-03-cleaning` | Bài p4-03 làm sạch dữ liệu (+ sửa 2 câu p4-01) | `1d52b9b` |
| 5 | `m3-p4-04-matplotlib` | Bài p4-04 vẽ biểu đồ (+ đặt Agg trong validate.py, conftest.py) | `325ec3d` |
| 6 | `m3-p4-05-sql` | Bài p4-05 SQLite | `0f1b004` |
| 7 | `m3-p4-06-project` | Mini-project phân tích dữ liệu | `53d9f44` |
| 7b | `m3-p4-review-fixes` | Sửa 25 điểm reviewer phase 4 | `12bbc47` |
| 8 | `m3-p4-test` | Phase test 4 | `0febc7a` |
| 9–13 | `m3-p5-0N-*` | Bài p5-01 … p5-05 | p5-01 `0b54b49`; p5-02 `d2416cf`; p5-03 `6bcb761`; p5-04 `7cd65aa`; p5-05 `8612c8f` |
| 13b | `m3-p5-review-fixes` | Sửa 38 điểm reviewer phase 5 (`tasks/m3-p5-review.md`) | `e0a633b` |
| 14 | `m3-p5-test` | Phase test 5 | `44d05fa` |
| 15 | `m3-mock-data-ml` | Mock exam Data & ML (boss viết blueprint chủ đề, review 100%) | `d9b7437` |
| 15b | `m3-visualizer-tables` | Visualize hiển thị DataFrame và mảng 2D dạng bảng nhỏ (hiện bị dồn một dòng, cắt "...") | `bc7ba47` |
| 15c | `m3-mcq-shuffle` | App chưa xáo lựa chọn mcq (question.tsx chỉ xáo parsons; CONTENT_GUIDE nói có xáo); xáo theo seed như parsons, giữ `shuffle_options: false` | `7cf05bc` |
| 16 | `m3-16-docs-vi` | Boss cập nhật `CLAUDE.md`, `docs/DESIGN.md`, review mẫu bản VI | `80f9579` (docs gitignore, chỉ commit 12 file .vi.md) |

Sau mỗi phase: subagent `reviewer` review nội dung trước khi chốt phase test.
