# SPEC: Global Search / Command Palette (`Ctrl+K` / `⌘K`)

## Tier & Summary
- **Tier:** **TIER 3** (touches Protected Zones: `tools/build_content.py`, `apps/web/src/lib/types.ts`, `apps/web/messages/{en,vi}.json`, plus 6+ files across Python build tooling and Next.js web UI).
- **Summary:** Add a zero-dependency, bilingual (EN/VI, diacritic-insensitive) Global Search Command Palette (`Ctrl+K` / `⌘K`) backed by a build-time static `search.json` index covering ready lessons, exercises, exams, glossary terms, interview questions, and portfolio briefs, with deep-link navigation and full Dose Design System compliance.

## Goal & Non-Goals
### Goal
1. Generate `apps/web/src/generated/search.json` inside `tools/build_content.py` containing compact, searchable metadata for all ready lessons/capstones, exercises, exams, glossary terms, interview questions, and portfolio briefs.
2. Implement a pure, zero-dependency bilingual search & ranking module (`apps/web/src/lib/search.ts`) with Vietnamese diacritic stripping (`đ` → `d`, NFD strip), multi-token matching across both EN and VI fields, category filtering, and lazy dynamic import of `search.json`.
3. Build `<CommandPalette />` (`apps/web/src/components/command-palette.tsx`) adhering strictly to `apps/web/design.md` (Dose theme), triggered by `Ctrl+K` / `⌘K` and via buttons in `AppShell` (desktop sidebar + mobile top bar), with full keyboard navigation (`↑`, `↓`, `Enter`, `Esc`).
4. Support clean client-side deep-links via `window.location.search` (no `useSearchParams()` to preserve Next.js `output: "export"` static builds without Suspense hazards) for exercises (`/lesson/<id>/?tab=exercises&ex=<exId>`), glossary (`/glossary/?q=<term>`), and interview questions (`/interview/?q=<id>`).
5. Maintain strict EN/VI i18n parity in `apps/web/messages/{en,vi}.json` and add Python unit tests in `tools/test_build_content.py`.

### Non-Goals
- Do NOT install any npm or Python packages (Dependency Freeze).
- Do NOT index full markdown lesson body prose or quiz questions (keeps `search.json` fast and lightweight).
- Do NOT modify `curriculum/` content files, `tools/validate.py`, `tools/schema/`, `apps/web/src/lib/storage.ts`, `apps/web/src/app/tokens.css`, or `apps/web/src/app/globals.css`.
- Do NOT use `useSearchParams()` in client pages (static export safety).

## File Whitelist
- `tools/build_content.py` (modify)
- `tools/test_build_content.py` (modify)
- `apps/web/src/lib/types.ts` (modify)
- `apps/web/src/lib/search.ts` (create)
- `apps/web/src/components/command-palette.tsx` (create)
- `apps/web/src/components/app-shell.tsx` (modify)
- `apps/web/src/components/lesson/lesson-view.tsx` (modify)
- `apps/web/src/app/(main)/glossary/page.tsx` (modify)
- `apps/web/src/app/(main)/interview/page.tsx` (modify)
- `apps/web/messages/en.json` (modify)
- `apps/web/messages/vi.json` (modify)

## File Blacklist
- `curriculum/**`
- `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock`, `apps/web/package.json`
- `tools/validate.py`, `tools/schema/**`, `tools/pyrunner/**`, `tools/localrunner/**`
- `apps/web/src/lib/storage.ts`, `apps/web/src/app/tokens.css`, `apps/web/src/app/globals.css`
- `.env*`

## Technical Design & Interface Contracts

### 1. Static Search Index (`tools/build_content.py` → `apps/web/src/generated/search.json`)
`build_content.main()` writes `out / "search.json"` with shape `{ "items": SearchItem[] }`.
Each `SearchItem` is a compact JSON object:
```ts
export type SearchKind = "lesson" | "exercise" | "glossary" | "interview" | "exam" | "portfolio";

export interface SearchItem {
  id: string;            // unique prefixed id, e.g. "lesson:p1-01-variables"
  kind: SearchKind;
  title: I18n;           // { en: string; vi?: string }
  subtitle?: I18n;       // concise summary/context (truncated <= 160 chars)
  href: string;          // app-relative path with trailing slash before query
  tags: string[];        // lowercase search tags (topics, phase, level, etc.)
  phase?: string;        // optional phase id ("p0".."p8", "cap")
}
```
Generation rules in `tools/build_content.py`:
- **Lessons & Capstones (`kind: "lesson"`):** Only for lessons where `built == True` (`ready == True`). `id = f"lesson:{lesson_id}"`, `title = meta["title"]`, `subtitle = meta.get("summary")`, `href = f"/lesson/{lesson_id}/"`, `tags = list(meta.get("tags") or [])`, `phase = group["id"]`.
- **Exercises (`kind: "exercise"`):** Collected from each built lesson's `lesson["exercises"]`. `id = f"exercise:{ex['id']}"`, `title = ex["title"]`, `subtitle = meta["title"]` (parent lesson title), `href = f"/lesson/{lesson_id}/?tab=exercises&ex={quote(ex['id'], safe='')}"`, `tags = list(ex.get("tags") or [])`, `phase = group["id"]`.
- **Exams (`kind: "exam"`):** From `exams` list. `id = f"exam:{exam['id']}"`, `title = exam["title"]`, `subtitle = exam.get("description")`, `href = "/placement/" if exam["kind"] == "placement" else f"/exam/{exam['id']}/"`, `tags = [t for t in (exam["kind"], exam.get("phase")) if t]`, `phase = exam.get("phase")` (omit if None).
- **Glossary (`kind: "glossary"`):** From `glossary.get("terms", [])`. `id = f"glossary:{term}"`, `title = {"en": term, **({"vi": f"{term} ({vi_term})"} if vi_term and vi_term != term else {})}`, `subtitle = {"en": _truncate(en, 160), **({"vi": _truncate(vi, 160)} if vi else {})}`, `href = f"/glossary/?q={quote(term, safe='')}"`, `tags = list(entry.get("tags") or [])`.
- **Interview (`kind: "interview"`):** From `interview.get("questions", [])`. `id = f"interview:{q['id']}"`, `title = {"en": _truncate(q["en"]["question"], 160), **({"vi": _truncate(q["vi"]["question"], 160)} if q.get("vi") else {})}`, `subtitle = {"en": f"{q['topic']} · {q['level']}", "vi": f"{q['topic']} · {q['level']}"}`, `href = f"/interview/?q={quote(q['id'], safe='')}"`, `tags = [t for t in (q.get("topic"), q.get("level"), q.get("kind")) if t]`.
- **Portfolio (`kind: "portfolio"`):** From `portfolio.get("projects", [])`. `id = f"portfolio:{proj['id']}"`, `title = proj["title"]`, `subtitle = proj.get("pitch")`, `href = "/portfolio/"`, `tags = list(dict.fromkeys([*(proj.get("tags") or []), *(proj.get("skills") or [])]))`, `phase = proj.get("phase")` (omit if None).
- Helper `_truncate(text: str, limit: int = 160) -> str`: collapses whitespace (`" ".join(text.split())`), trims to `limit` with `"…"` if longer.
- Update `build_lesson_summary` (or a clean helper) so exercises from built lessons are passed back without breaking existing callers/tests.

### 2. Search Engine (`apps/web/src/lib/search.ts`)
Exports:
- `SEARCH_KINDS: readonly SearchKind[] = ["lesson", "exercise", "glossary", "interview", "exam", "portfolio"]`
- `type SearchFilter = "all" | SearchKind`
- `normalizeSearchText(input: string): string` — NFD normalize, strip `/[\u0300-\u036f]/g`, replace `/đ/gi` with `"d"`, lowercase, collapse whitespace.
- `loadSearchIndex(): Promise<SearchItem[]>` — memoized dynamic import safe in static export + GitHub Pages `basePath`, with explicit typing so TypeScript does not fail on JSON literal narrowing:
  ```ts
  const mod = (await import("@/generated/search.json")) as {
    default?: { items?: SearchItem[] };
    items?: SearchItem[];
  };
  return mod.items ?? mod.default?.items ?? [];
  ```
- `export const DEEPLINK_EVENT = "pyai:deeplink";` — custom window event name dispatched by `<CommandPalette />` after `router.push(item.href)` with `{ detail: { href: item.href } }` so same-route pages immediately re-parse query parameters without remounting.
- `searchItems(items: readonly SearchItem[], query: string, filter: SearchFilter = "all", limit = 30): SearchItem[]`:
  - Filter by `filter !== "all"` first.
  - If normalized query is empty, return empty array (UI shows Quick Links / prompt).
  - Split normalized query into whitespace tokens. Every token must match at least one field (`title.en`, `title.vi`, `tags`, `subtitle.en`, `subtitle.vi`, `phase`).
  - Scoring (higher is better):
    - Exact title match (`en` or `vi`): +100
    - Title starts with full query: +60
    - Title contains full query: +35
    - Per-token in title: +20
    - Per-token in tags / phase: +12
    - Per-token in subtitle: +6
  - Sort descending by score, tie-break by kind priority (`lesson`, `exercise`, `exam`, `glossary`, `interview`, `portfolio`) then `title.en`. Slice to `limit`.

### 3. Command Palette UI (`apps/web/src/components/command-palette.tsx`) & `AppShell` (`apps/web/src/components/app-shell.tsx`)
- Props: `export function CommandPalette({ open, onOpenChange }: { open: boolean; onOpenChange: (open: boolean) => void })`
- Global shortcut listener inside `CommandPalette` (or `AppShell`): `keydown` for `(e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k"` (ignore when `e.altKey || e.isComposing`), calls `e.preventDefault()` and toggles `open`.
- Lazy-loads `loadSearchIndex()` on first open (shows loading text from `search.loading` while fetching).
- Uses Radix `Dialog` + `DialogContent` from `@/components/ui/dialog` (`p-0 gap-0 max-w-2xl overflow-hidden`, NO outer `border` class — Dose floating elevation uses `bg-popover` + `shadow-[var(--shadow-lift)]` only), visually hidden `DialogTitle` & `DialogDescription` (`sr-only`) for a11y.
- Search input autofocused on open, with `Search` icon and clear button when query non-empty (`aria-label={t("clear")}`). **Do NOT render a duplicate close button** — `DialogContent` already renders a built-in top-right close (`X`) button at `right-3.5 top-3.5`; reserve `pr-12` on the search input row so the clear button never overlaps the built-in close button.
- Filter pill bar (`all` + `SEARCH_KINDS`) with `hit` tap target (≥ 44px), `aria-pressed`, horizontal scroll on mobile without page overflow.
- Keyboard navigation:
  - `ArrowDown` / `ArrowUp` cycles `activeIndex` across visible items (or Quick Jump items when query is empty) and scrolls active row into view.
  - `Enter` navigates to active item's `href` via `router.push(item.href)`, dispatches `window.dispatchEvent(new CustomEvent(DEEPLINK_EVENT, { detail: { href: item.href } }))`, and closes dialog.
  - Reset `activeIndex` to `0` whenever `query` or `filter` changes; clear `query` & `filter` when closing.
- When `query.trim() === ""`: show 6 Quick Jump links (Roadmap `/learn/`, Review `/review/`, Exams `/exams/`, Playground `/playground/`, Glossary `/glossary/`, Interview `/interview/`) so the palette is immediately actionable.
- Footer bar with keyboard hints (`↑↓`, `Enter`, `Esc`) and result count.
- **Dose Design System strict rules:**
  - Zero raw color literals (`#hex`, `oklch(...)`, `rgb(...)`).
  - Zero `backdrop-blur`, zero `transition-all`.
  - Only `font-normal`, `font-medium`, `font-bold` (no `font-semibold`/`font-black`).
  - Tap targets ≥ 44px via `.hit` on small controls; `aria-hidden="true"` on decorative icons; `aria-label` on icon-only buttons.
- **`AppShell` triggers:**
  - Desktop sidebar (between `<Link href="/">` logo and `<nav>`): full-width button showing `Search` icon, `t("search")`, and `<kbd>` showing `Ctrl K` (or `⌘K` on macOS detected safely in `useEffect` to avoid hydration mismatch).
  - Mobile top bar: icon-only button (`hit`) with `Search` icon and `aria-label={t("search")}` placed inside the right utility cluster.

### 4. Deep-Link Handling (Static-Export & Same-Route Safe — NO `useSearchParams`)
All three targets listen to initial mount (or `meta.id` change), `popstate`, AND `"pyai:deeplink"` custom events (parsing query params from `(event as CustomEvent<{ href?: string }>).detail?.href` via `new URL(href, window.location.origin).search` when available, falling back to `window.location.search`).
- **`apps/web/src/components/lesson/lesson-view.tsx`:** Parse `tab` and `ex`:
  - If `ex` matches an exercise in `lesson.exercises`, set `exerciseId(ex)`, `setTab("exercises")`, and `setMobilePane("content")`.
  - Else if `tab` is `"theory" | "examples" | "exercises" | "quiz"`, set `setTab(tab)` and `setMobilePane("content")`.
- **`apps/web/src/app/(main)/glossary/page.tsx`:** Parse `q`; if non-empty, call `setTag(null)` (clear active tag filter so the target term is never masked) and `setQuery(q)`.
- **`apps/web/src/app/(main)/interview/page.tsx`:** Parse `q`; if it matches a question `id` in `questions`, call `setTopic(null)` (clear active topic filter so the target question is rendered), `setOpen((o) => ({ ...o, [q]: true }))`, and `requestAnimationFrame(() => document.getElementById(\`accordion-trigger-${q}\`)?.scrollIntoView({ behavior: "smooth", block: "center" }))`.

### 5. i18n Keys (`apps/web/messages/en.json` & `apps/web/messages/vi.json`)
Add `"search"` namespace to BOTH files with identical keys:
- `open`, `title`, `description`, `placeholder`, `clear`, `loading`, `empty`, `quickJump`, `resultsCount` (`"{count} results"` / `"{count} kết quả"`), `hintNavigate`, `hintSelect`, `hintClose`
- `kinds`: `{ "all", "lesson", "exercise", "glossary", "interview", "exam", "portfolio" }`
Also add `"nav.search"` (`"Search"` / `"Tìm kiếm"`) to both files.
Vietnamese prose must address the user as `"bạn"` if any pronoun appears (never `"ta"`/`"chúng ta"`).

## Verification Commands
1. `uv run ruff check tools/build_content.py tools/test_build_content.py`
2. `uv run python -m pytest tools/test_build_content.py -q`
3. `uv run python -m pytest tools -q`
4. `pnpm.cmd --filter web typecheck` (regenerates `search.json` + runs `tsc --noEmit` + checks EN/VI i18n parity)
5. `pnpm.cmd --filter web build` (verifies static export succeeds cleanly)
6. Dose static grep check on new/modified `.tsx` files: no `#hex`/`oklch`/`rgb(`, no `backdrop-blur`, no `transition-all`, no `font-semibold`/`font-black`.
