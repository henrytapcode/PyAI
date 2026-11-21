# Handoff: Python for AI Engineer platform (M2, phases 2-3)

Ngày: 2026-10-23. Nhánh: `m2/revision-phases-1-3` (chưa push, chưa có PR). Cây làm việc sạch ở commit `d743b5f`.

## 1. Bối cảnh

- Dự án: nền tảng học Python song ngữ VI/EN cho AI Engineer. Đọc `CLAUDE.md`, `docs/DESIGN.md`, `docs/CONTENT_GUIDE.md` trước khi làm.
- Kế hoạch đã duyệt: `C:\Users\Henry\.claude\plans\typed-chasing-flamingo.md` (phase 2 = 9 bài, phase 3 = 5 bài, phase test, glossary, interview, placement, gate cuối).
- Transcript đầy đủ của session cũ: `C:\Users\Henry\.claude\projects\C--Users-Henry-Desktop-python-ai-platform\c6b6877a-0170-48b7-bf4f-fccd8022eb72.jsonl`.

## 2. Đã làm (đã commit)

| Commit | Nội dung |
|---|---|
| `7637b44` | p2-09-mini-project (expense tracker), đã sửa 18 findings từ review |
| `786ed61` | Glossary: `validation`, `ISO date`, `round trip`, `frozen dataclass` |
| `224d6b1` | Phase test p2: id `p2-phase-test`, 15 câu, pass 0.7, 25 phút |
| `f9eb156` | Interview bank: +10 câu (iv-78..iv-87), mục "Python intermediate (more)" |
| `c2c1801` | p3-01-pytest hoàn chỉnh (thêm ex02 debug + quiz) |
| `d9e308c` | p3-03-logging hoàn chỉnh (lesson.vi, ex02 fill, quiz) |
| `d743b5f` | p3-02-ruff hoàn chỉnh (meta, 2 exercise, quiz) |

Phase 1 (10 bài) và phase 2 (9 bài + phase test) đã xong; phase 2 đã qua reviewer.
Phase 3: p3-01, p3-02, p3-03 đã viết xong, validate 0 lỗi, pytest + ruff sạch, **chưa qua reviewer**.

## 3. Đang làm

Không có việc dở. Đã dừng theo yêu cầu để chờ reset giới hạn 5 giờ (reset khoảng 14:20 UTC ngày 2026-10-23).

## 4. Chưa làm / sắp làm (theo thứ tự)

1. **p3-04-debugging** (prerequisites `[p3-03-logging, p1-10-exceptions]`): đọc traceback, bisect bằng print/log, `breakpoint()`/pdb, VS Code debugger, rubber duck. 2 exercise `debug` (tìm bug; tái hiện rồi sửa). Dùng Visualize nhiều. Lệnh terminal để trong fence `bash`.
2. **p3-05-mini-project** (prerequisites `[p3-04-debugging, p2-04-dataclasses]`): text-cleaning toolkit (hàm thuần, dataclass config, logging, parametrized tests). 2 task `project`, mỗi task cần ≥1 alternative.
3. **Review gộp một lần** p3-01..p3-05 bằng agent `reviewer` (chỉ đọc), rồi sửa findings và commit.
4. **Phase test p3**: 12-15 câu, Parsons không trạng thái, không `import pytest` trong output/fill/parsons.
5. **Placement**: bổ sung `curriculum/placement/placement.yaml` (Track B chỉ được bỏ qua phase 0-1, giữ nguyên luật skip).
6. Tùy chọn: thêm glossary p3 (linter, formatter, log level, breakpoint, fixture...).
7. **Gate cuối**: `uv run python tools/validate.py`, `uv run pytest curriculum`, `uv run ruff check curriculum`, `pnpm --filter web typecheck`, `pnpm --filter web build`; smoke test trình duyệt một bài p2 (Visualize trên class và generator); cập nhật dòng trạng thái trong `CLAUDE.md`; commit.
8. Push/PR chỉ khi người dùng yêu cầu.

## 5. Ràng buộc người dùng đã chốt

- Chạy tuần tự, **không chạy 3 agent song song**; làm trực tiếp cho tiết kiệm.
- Chừa khoảng 5% cuối của phiên 5h; hết thì chờ reset rồi tiếp tục. Kiểm tra bằng `mcp__ccd_session_mgmt__get_usage` (cần nạp qua ToolSearch). Lúc gần cuối, weekly đã dùng ~48-49%.
- Commit nhỏ, mỗi commit một việc.
- Mỗi lần sau khi sửa file, hook chạy validate; lỗi giữa chừng khi bài chưa đủ file là bình thường, bỏ qua cho đến khi đủ bộ.

## 6. Quy tắc nội dung cần nhớ (đã gây lỗi trước đây)

- Mỗi bài: `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, 2-3 example (`.py`, `.out`, `.en.md`, `.vi.md`), 2 exercise, `quiz.yaml`.
- Quiz: 15-18 câu, mỗi loại mcq/output/fill/parsons ≥2 (tôi dùng 15 câu: 6 mcq, 4 output, 3 fill, 2 parsons), 6 flashcard, đều có explanation.
- **Parsons phải có đúng MỘT thứ tự hợp lệ.** Validator chạy mọi hoán vị trong cùng một process, nên code có trạng thái toàn cục (mức logger, `basicConfig`, logger đặt tên) gây báo sai "another valid order". Dùng code không trạng thái. Tránh các dòng cùng thụt lề có thể đổi chỗ, hoặc `print` cho cùng output trước/sau một `assert`. Validator bỏ qua dòng bắt đầu bằng `while`.
- Mọi khái niệm trong quiz/hint phải được dạy trong bài hoặc bài tiên quyết.
- Test exercise chỉ dùng: assert, `pytest.raises`, `approx`, `parametrize`, `capsys`, `tmp_path`, `caplog`, `monkeypatch`, fixture khai báo trong file test. Không `import pytest` trong code output/fill/parsons (runner trình duyệt).
- Exercise: ít nhất 1 `fill` hoặc `debug` mỗi bài; hint đúng 3 tầng mỗi ngôn ngữ (tầng 3 là khung code có chỗ trống nhỏ); `code`/`project` cần ≥1 alternative.
- VI giữ thuật ngữ tiếng Anh kèm giải nghĩa; code block giống hệt giữa EN/VI trừ comment `#`; mermaid cùng số dòng; mỗi bài có đúng một lời mời Visualize; ≥2 yếu tố trực quan.
- Ruff per-file-ignores cho phép lỗi cố ý trong starter (F821, F841, B006, E722, F401...).

## 7. Mẹo công cụ

- Bash từ chối heredoc lớn: dùng Write ra file (scratchpad hoặc đích) rồi `cat >>`. Write tự tạo thư mục cha.
- File có lẫn CRLF/LF, git cảnh báo nhưng vô hại.
- `ruff format --check` báo 16 file; dự án chỉ yêu cầu `ruff check`.
- Agent đã bị người dùng dừng thì không resume được; chỉ khởi chạy agent mới khi người dùng yêu cầu rõ.

## 8. Lệnh kiểm tra nhanh

```bash
uv run python tools/validate.py --path curriculum/phase-03-code-quality/p3-04-debugging
uv run pytest curriculum/phase-03-code-quality
uv run ruff check curriculum
```

## 9. Cách bắt đầu session mới

Gõ: "Đọc handoff.md rồi tiếp tục từ p3-04-debugging." Bước đầu tiên: kiểm tra usage, đối chiếu cấu trúc p3-01 hoặc p3-03 làm mẫu, rồi viết p3-04.
