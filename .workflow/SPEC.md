# SPEC — Bookmarks & Markdown Notes per Lesson

## Tier & Summary
- **Tier:** **TIER 2 (Standard)** — Touches 6 files within `apps/web` (1 store file, 1 new component, 2 existing UI files, 2 i18n files), zero protected backend/curriculum pipeline changes, backward-compatible `localStorage` persistence.
- **Summary:** Add per-lesson Bookmarks and Markdown Notes stored in `useProgress` (`localStorage` + automatic JSON export/import), accessible via a Bookmark toggle and `Notes` tab in `LessonView`, and filterable on `/learn/` (`All` / `Bookmarked` / `With notes`).

## Goal & Non-Goals
- **Goals:**
  1. Persist `bookmarks` and `notes` per `lessonId` in `useProgress` (`apps/web/src/lib/progress.ts`) with full backward compatibility for existing v1 `localStorage` data and automatic inclusion in `exportProgress()` / `importData()`.
  2. Provide a header Bookmark toggle button and a `Notes` tab (`?tab=notes` deep-link supported) in `LessonView`.
  3. Build `LessonNotes` with Edit / Preview modes (reusing `<Markdown />` with `onTryCode` so Python snippets in notes can run in Workbench), 400ms debounced autosave + unmount/lesson-change flush, `.md` download export, and inline 2-step clear confirmation (no `window.confirm`).
  4. Add a Dose-compliant filter bar (`All`, `Bookmarked`, `With notes`) and per-row bookmark/note indicators + note excerpt preview on `/learn/`.
  5. Maintain strict 1:1 EN/VI i18n parity (VI addresses reader as `"bạn"`) and Dose Design System compliance (`apps/web/design.md`).
- **Non-Goals (DO NOT touch):**
  - Do NOT touch `tools/`, `curriculum/`, `packages/`, `apps/web/src/lib/storage.ts`, `apps/web/src/lib/types.ts`, `apps/web/src/app/tokens.css`, `apps/web/src/app/globals.css`, or `apps/web/src/components/markdown.tsx`.
  - Do NOT bump `ProgressData.version` from `1` or break existing persisted state missing `bookmarks`/`notes`.
  - Do NOT install new npm packages.

## File Whitelist
- `apps/web/src/lib/progress.ts` (modify)
- `apps/web/src/components/lesson/lesson-notes.tsx` (create)
- `apps/web/src/components/lesson/lesson-view.tsx` (modify)
- `apps/web/src/app/(main)/learn/page.tsx` (modify)
- `apps/web/messages/en.json` (modify)
- `apps/web/messages/vi.json` (modify)

## File Blacklist
- `apps/web/src/lib/storage.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/components/markdown.tsx`
- `apps/web/src/app/tokens.css`
- `apps/web/src/app/globals.css`
- `apps/web/package.json`, `pnpm-lock.yaml`
- Everything under `tools/`, `curriculum/`, `packages/`

## Technical Design & Interface Contracts

### 1. Persistence Contract (`apps/web/src/lib/progress.ts`)
Add type and fields to `ProgressData` (keeping `version: 1`):
```ts
export interface LessonNote {
  content: string;
  updatedAt: string; // ISO timestamp
}
```
Inside `ProgressData`:
```ts
  /** Bookmarked lesson IDs mapped to ISO timestamp when bookmarked. */
  bookmarks: Record<string, string>;
  /** Per-lesson Markdown notes mapped by lesson ID. */
  notes: Record<string, LessonNote>;
```
Inside `initialProgress()`:
```ts
  bookmarks: {},
  notes: {},
```
Inside `Actions`:
```ts
  toggleBookmark(lessonId: string): void;
  saveNote(lessonId: string, content: string): void;
  deleteNote(lessonId: string): void;
```
Behavior & edge cases:
- Always guard legacy persisted states where `s.bookmarks` or `s.notes` may be `undefined` (`const prev = s.bookmarks ?? {}`, `const prev = s.notes ?? {}`).
- `toggleBookmark(lessonId)`: if `prev[lessonId]` exists, omit `lessonId` from new object; otherwise set `next[lessonId] = new Date().toISOString()`.
- `saveNote(lessonId, content)`: if `content.trim().length === 0`, omit `lessonId` from `notes` (clean empty notes); otherwise set `next[lessonId] = { content, updatedAt: new Date().toISOString() }`.
- `deleteNote(lessonId)`: omit `lessonId` from `notes`.
- `importData(data)`: `{ ...initialProgress(), ...data, bookmarks: data.bookmarks ?? {}, notes: data.notes ?? {} }`.

### 2. `LessonNotes` Component (`apps/web/src/components/lesson/lesson-notes.tsx`)
```tsx
export function LessonNotes({
  lessonId,
  lessonTitle,
  onTryCode,
}: {
  lessonId: string;
  lessonTitle: string;
  onTryCode: (code: string) => void;
})
```
- Reads `saved = useProgress((s) => s.notes?.[lessonId])`, `saveNote = useProgress((s) => s.saveNote)`, `deleteNote = useProgress((s) => s.deleteNote)`.
- Maintains local `draft` state synced when `lessonId` changes (and flushes any pending debounced save for the previous `lessonId` before switching or unmounting).
- Debounced autosave (400ms) calls `saveNote(lessonId, nextText)` and updates a subtle status label (`lesson.noteSaved` / `lesson.noteSaving` / empty).
- Mode toggle (`Edit` / `Preview`) using two `.hit` pill buttons with `aria-pressed` (no nested Radix `<Tabs>`).
- **Edit mode:** `<textarea>` with `min-h-[320px] w-full resize-y rounded-lg border border-border bg-card p-4 font-mono text-sm leading-relaxed text-foreground placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`, `aria-label={t("notes")}`, placeholder from `t("notePlaceholder")`. Footer shows subtle Markdown hint + character count.
- **Preview mode:** If `draft.trim()` is non-empty, renders `<div className="rounded-lg border border-border bg-card p-5"><Markdown text={draft} onTryCode={onTryCode} canVisualize={false} /></div>`. If empty, shows an empty-state card with button to switch to Edit mode.
- **Export `.md`:** Downloads a `Blob` (`text/markdown;charset=utf-8`) named `${lessonId}-notes.md` prefixed with `# ${lessonTitle}\n\n${draft}`, disabled when `draft.trim().length === 0`.
- **Clear note:** Inline 2-step confirmation (`Clear` -> `Confirm clear` / `Cancel`), disabled when `draft.trim().length === 0`. Never use `window.confirm`.
- **Dose compliance:** Zero raw hex/oklch literals, zero `backdrop-blur`, zero `transition-all`, font weights only `400/500/700` (`font-normal`/`font-medium`/`font-bold`), all interactive controls use `.hit` or `Button` (`>= 44px` tap target).

### 3. `LessonView` Integration (`apps/web/src/components/lesson/lesson-view.tsx`)
- Extend `type Tab = "theory" | "examples" | "exercises" | "quiz" | "notes";`
- Extend `applySearch` to accept `nextTab === "notes"`.
- In `<header>` (next to prev/next buttons): add Bookmark toggle `<Button variant="ghost" size="icon-sm" onClick={() => toggleBookmark(meta.id)} aria-pressed={isBookmarked} aria-label={isBookmarked ? t("removeBookmark") : t("addBookmark")} title={...}>` with `<Bookmark className={cn("size-4", isBookmarked && "fill-current text-primary")} aria-hidden="true" />`.
- In `<TabsList>`: update grid class to `grid-cols-5 sm:flex sm:w-full sm:justify-start` and add `<TabsTrigger value="notes">`:
  - Icon `<StickyNote aria-hidden="true" className={cn(hasNote && "text-primary")} />` + label `{t("notes")}` + subtle indicator dot when `hasNote` (`<span className="size-1.5 rounded-full bg-primary" aria-hidden="true" />`).
- Add `<TabsContent value="notes" className="animate-rise">` rendering `<LessonNotes lessonId={meta.id} lessonTitle={loc.t(meta.title)} onTryCode={tryCode} />`.

### 4. Roadmap Filter & Indicators (`apps/web/src/app/(main)/learn/page.tsx`)
- Add local filter state: `type LearnFilter = "all" | "bookmarked" | "notes";` defaulting to `"all"`.
- Compute counts across ready lessons in `catalog.phases` (and capstones if applicable, or phases lessons): `bookmarkedCount`, `notesCount`.
- Render a compact filter bar below `PageHeader` (and after Track B card if visible) with 3 `.hit` pill buttons (`role="group"`, `aria-label={t("filterLabel")}`, `aria-pressed`):
  - `t("filterAll")`
  - `t("filterBookmarked")` + count badge when `bookmarkedCount > 0`
  - `t("filterNotes")` + count badge when `notesCount > 0`
- On each ready lesson row:
  - If `Boolean(p.bookmarks?.[l.id])`, render `<Bookmark className="size-3.5 shrink-0 fill-current text-primary" aria-label={t("bookmarkedBadge")} />` next to the lesson title.
  - If `Boolean(p.notes?.[l.id]?.content?.trim())`, render `<StickyNote className="size-3.5 shrink-0 text-primary" aria-label={t("hasNoteBadge")} />` next to the lesson title.
  - When `filter === "notes"` and note exists, render a 1-line excerpt (`line-clamp-1 text-xs text-muted-foreground mt-1`) of the first non-empty line (stripped of leading `#`/`>`/`-`/`*` markdown chars) and link directly to `/lesson/${l.id}/?tab=notes` (while `all`/`bookmarked` keep `/lesson/${l.id}/`).
- When `filter !== "all"`:
  - Filter `phase.lessons` to matching ready lessons; hide phases with 0 matching lessons; hide `prog.phaseTest` row.
  - If 0 phases match, render a Dose `<Card className="p-8 text-center">` empty state (`t("emptyBookmarked")` or `t("emptyNotes")`) with a `<Button variant="outline" size="sm" onClick={() => setFilter("all")}>{t("showAll")}</Button>`.

### 5. i18n Keys (`apps/web/messages/en.json` & `apps/web/messages/vi.json`)
Add identical keys to both files:
- Under `learn`:
  - `filterLabel`: EN `"Filter lessons"` | VI `"Lọc bài học"`
  - `filterAll`: EN `"All"` | VI `"Tất cả"`
  - `filterBookmarked`: EN `"Bookmarked"` | VI `"Đã lưu"`
  - `filterNotes`: EN `"With notes"` | VI `"Có ghi chú"`
  - `bookmarkedBadge`: EN `"Bookmarked"` | VI `"Đã đánh dấu"`
  - `hasNoteBadge`: EN `"Has notes"` | VI `"Có ghi chú"`
  - `emptyBookmarked`: EN `"No bookmarked lessons yet. Open any lesson and click the bookmark icon to save it here."` | VI `"Chưa có bài học nào được lưu. Mở một bài học và bấm biểu tượng đánh dấu để lưu vào đây."`
  - `emptyNotes`: EN `"No lesson notes yet. Open any lesson and switch to the Notes tab to write Markdown notes."` | VI `"Chưa có ghi chú nào. Mở một bài học và chuyển sang tab Ghi chú để viết ghi chú Markdown."`
  - `showAll`: EN `"Show all lessons"` | VI `"Hiện tất cả bài học"`
- Under `lesson`:
  - `notes`: EN `"Notes"` | VI `"Ghi chú"`
  - `addBookmark`: EN `"Bookmark lesson"` | VI `"Đánh dấu bài học"`
  - `removeBookmark`: EN `"Remove bookmark"` | VI `"Bỏ đánh dấu bài học"`
  - `noteEdit`: EN `"Edit"` | VI `"Viết"`
  - `notePreview`: EN `"Preview"` | VI `"Xem trước"`
  - `notePlaceholder`: EN `"Write your Markdown notes for this lesson…\n\nSupports headings, lists, > [!TIP] callouts, and ```python code blocks (clickable Try it in Preview)."` | VI `"Viết ghi chú Markdown của bạn cho bài học này…\n\nHỗ trợ tiêu đề, danh sách, hộp > [!TIP] và khối code ```python (bấm Chạy thử ngay ở chế độ Xem trước)."`
  - `noteSaved`: EN `"Saved"` | VI `"Đã lưu"`
  - `noteSaving`: EN `"Saving…"` | VI `"Đang lưu…"`
  - `noteExport`: EN `"Export .md"` | VI `"Xuất .md"`
  - `noteClear`: EN `"Clear"` | VI `"Xóa"`
  - `noteClearConfirm`: EN `"Confirm clear"` | VI `"Xác nhận xóa"`
  - `noteEmptyPreview`: EN `"Nothing to preview yet. Switch to Edit to start writing your notes."` | VI `"Chưa có nội dung để xem trước. Chuyển sang tab Viết để bắt đầu ghi chú của bạn."`
  - `noteChars`: EN `"{count} chars"` | VI `"{count} ký tự"`
  - `noteHint`: EN `"Markdown supported · saved locally in your browser"` | VI `"Hỗ trợ Markdown · tự động lưu trên trình duyệt của bạn"`

## Verification Commands
1. Typecheck: `pnpm.cmd --filter web typecheck`
2. Build: `pnpm.cmd --filter web build`
3. Dose static check: verify 0 raw `#hex`/`oklch`, 0 `backdrop-blur`, 0 `transition-all`, 0 `font-semibold` across modified `.tsx` files.
4. Browser E2E verification on served `apps/web/out`:
   - Open `/lesson/p1-01-variables/`, toggle Bookmark, switch to `Notes` tab, write Markdown with a Python code block, verify `Saved`, switch to `Preview` and verify rendered Markdown + `Try it` button, reload page and verify persistence, navigate to `/learn/` and verify `Bookmarked` & `With notes` filters + indicators in both EN and VI with 0 console errors.
