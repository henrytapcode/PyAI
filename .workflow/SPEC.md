# SPEC: Smart Weak-Topic Drill & Interactive Mock Interview

## Tier & Summary
- **Tier:** TIER 2 (Standard — frontend-only feature inside `apps/web`, zero schema/storage/backend/curriculum changes; touches 8 files including 2 new components and EN/VI message parity).
- **Summary:** Add two high-value practice modes using existing `review.json` (958 tagged questions) and `interview.json` (87 questions with `kind` and `tip`):
  1. **Smart Weak-Topic Drill** as a tab inside `/review/` (plus 1-click deep links from Dashboard Weak Topics).
  2. **Interactive Mock Interview** as a tab inside `/interview/` with setup filters, per-question timer, scratchpad notes, progressive tip reveal, model answer comparison, and 3-level self-rating.

## Goal & Non-Goals
- **Goals:**
  - Let learners drill their weakest topics (derived from `questionStats` via `topicAccuracy`) or any chosen topic with 5/10/15 questions from `review.json`, updating `questionStats`, `srs` (adding missed questions), and `xp`.
  - Deep-link from Dashboard weak topics directly into `/review/?mode=drill&topic=<topicId>` (and `/review/?mode=drill`).
  - Let learners run timed, realistic mock interviews from `interview.json` with filters (`topic`, `level`, `kind`, `count`, `timer`), scratchpad notes, optional tip reveal, model answer reveal, 3-level self-assessment (`needs_work` | `partial` | `confident`), and end-of-session summary.
  - Surface existing `kind` badge and `tip` callout on the Interview Question Bank as well.
  - Follow Dose Design System (`apps/web/design.md`): no raw color literals, no `backdrop-blur`, no `transition-all`, tap targets >= 44px (`.hit`), full EN/VI parity (`"bạn"` in VI).
- **Non-Goals (DO NOT touch):**
  - Do NOT modify `ProgressData` persisted schema or `apps/web/src/lib/storage.ts`.
  - Do NOT modify `tools/build_content.py`, `curriculum/`, `apps/web/src/lib/types.ts`, `tokens.css`, or `globals.css`.
  - Do NOT add new top-level navigation routes or install npm packages.
  - Do NOT add AI/network calls (app is 100% static/offline-first).

## File Whitelist
- `apps/web/src/lib/progress.ts` (add `recordDrill` and `setPracticed` actions only)
- `apps/web/src/components/weak-topic-drill.tsx` (NEW)
- `apps/web/src/components/mock-interview.tsx` (NEW)
- `apps/web/src/app/(main)/review/page.tsx`
- `apps/web/src/app/(main)/interview/page.tsx`
- `apps/web/src/app/(main)/page.tsx`
- `apps/web/messages/en.json`
- `apps/web/messages/vi.json`

## File Blacklist
- `apps/web/src/lib/storage.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/tokens.css`
- `apps/web/src/app/globals.css`
- `tools/**`
- `curriculum/**`
- `packages/**`
- `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock`

## Technical Design & Interface Contracts

### 1. Store Actions (`apps/web/src/lib/progress.ts`)
Add two additive actions to `Actions` (no changes to `ProgressData` or `initialProgress`):
```ts
recordDrill(answers: AnswerRecord[]): void;
setPracticed(id: string, value: boolean): void;
```
- `recordDrill(answers)`:
  - Calls existing `applyAnswers(s, answers)` to update `questionStats` and enqueue missed questions (`q:<id>`) into `srs`.
  - Awards `XP.review * correctCount` via `gain(s, ...)` (if `correctCount > 0`, else no XP change).
- `setPracticed(id, value)`:
  - Sets `practiced: { ...s.practiced, [id]: value }` idempotently (used when learner self-rates `"confident"` in Mock Interview so it never accidentally un-marks an already practiced question).

### 2. Smart Weak-Topic Drill (`apps/web/src/components/weak-topic-drill.tsx`)
```ts
export interface WeakTopicDrillProps {
  questions: Question[];
  initialTopic?: string | null;
}
```
- **Smart Question Selection (`buildDrillQueue`):**
  - Pure helper function taking `(questions, progress, selectedTopic: string | "smart", count: 5 | 10 | 15)`.
  - Filter pool:
    - If `selectedTopic !== "smart"`: questions where `q.tags.includes(selectedTopic)`.
    - If `selectedTopic === "smart"`: rank topics by `topicAccuracy(p)` ascending (weakest first). Take questions whose primary tag (`q.tags[0]`) is in weak topics (`rate < 0.7`) first; if fewer than `count`, top up from remaining lowest-accuracy topics, then unseen topics (shuffled within each priority bucket).
  - Within a bucket, prioritize questions with higher `wrong` count or never attempted (`!p.questionStats[q.id]`), then shuffle ties.
  - Slice to `Math.min(count, pool.length)`.
- **States:**
  - `setup`: Shows weak-topic accuracy cards (top weak topics with progress bars + 1-click select), topic filter chips (`Smart mix` + topics present in `questions` sorted with weakest first), length selector (`5`, `10`, `15`), and `Start drill` CTA (disabled if pool is empty).
  - `active`: Progress bar (`pos + 1 / queue.length`), `QuestionView` (`showType={false}`), `SourceLine` with topic badge + lesson link, `Check` button -> reveals explanation + `Next` / `Finish` button. Records each answer into session results; on finish (or last question submit), calls `recordDrill(answers)` once.
  - `summary`: Score (`correct/total`, `%`), XP earned, per-topic session breakdown, list of missed questions with lesson links, and actions: `Drill again` (same config) & `Change topic`.
- **Edge Cases:**
  - New learner (`questionStats` empty): `Smart mix` gracefully falls back to a balanced random sample across available topics with an explanatory hint.
  - `initialTopic` passed from URL `?mode=drill&topic=X`: pre-selects topic `X` if valid and exists in `questions`.

### 3. Interactive Mock Interview (`apps/web/src/components/mock-interview.tsx`)
```ts
export interface MockInterviewProps {
  questions: InterviewQuestion[];
}
```
- **Setup State:**
  - Filters: `topic` (`"all"` | specific topic), `level` (`"all"` | `"junior"` | `"mid"`), `kind` (`"all"` | `"concept"` | `"coding"` | `"scenario"` | `"system"`), `count` (`3` | `5` | `8`), `timerSec` (`0` | `120` | `300`).
  - Shows live matching pool count; disables Start if `0` matches.
  - Prioritizes unpracticed questions first when building the session queue, then shuffles.
- **Active State:**
  - Header row: question index (`1/5`), progress bar, topic + level + kind badges, and countdown timer (`MM:SS` in `font-mono tabular-nums`) with Pause/Resume button (when `timerSec > 0`). When timer hits `0`, displays a non-blocking `Time's up` badge (never auto-skips).
  - Prompt: `Markdown` question + optional `StaticCode` block.
  - Progressive Tip: collapsible `Show tip` button revealing `qa.value.tip` (when present).
  - Scratchpad: `<textarea>` for learner's outline/notes (ephemeral per question in session state).
  - Reveal Model Answer: reveals `qa.value.answer` alongside the learner's notes, plus 3 self-rating buttons:
    - `needs_work` ("Needs work" / "Cần ôn thêm")
    - `partial` ("Partially" / "Tạm ổn")
    - `confident` ("Confident" / "Tự tin") -> calls `setPracticed(q.id, true)`.
  - Selecting a rating advances to next question (or summary on last question).
- **Summary State:**
  - Totals for `Confident`, `Partially`, `Needs work`, and total elapsed time.
  - Expandable review list of `Needs work` / `Partially` questions showing model answer + tip.
  - Actions: `Start new mock` (back to setup) and `Retry missed` (if any `needs_work` items exist).

### 4. Page Integrations
- **`apps/web/src/app/(main)/review/page.tsx`:**
  - Wrap content in `Tabs` (`srs` | `drill`).
  - Read `window.location.search` on mount (`?mode=drill&topic=...`) to activate `drill` tab and pass `initialTopic` to `<WeakTopicDrill />`.
  - Keep existing SRS review logic completely intact inside the `srs` tab.
- **`apps/web/src/app/(main)/interview/page.tsx`:**
  - Wrap content in `Tabs` (`bank` | `mock`).
  - Keep deep-link `?q=<id>` opening the `bank` tab and expanding that accordion item.
  - In `bank` tab, also render `q.kind` badge (if present) and `qa.value.tip` callout (if present) inside the expanded panel.
- **`apps/web/src/app/(main)/page.tsx` (Dashboard):**
  - On each weak topic row in the Weak Topics card, make the topic row link (or add a compact icon/link) to `/review/?mode=drill&topic=${encodeURIComponent(w.topic)}`, and add a `Drill weak topics` button pointing to `/review/?mode=drill` when `data.accuracy.length > 0`.

### 5. i18n Parity (`apps/web/messages/{en,vi}.json`)
- Add matching keys in both `en.json` and `vi.json`:
  - `review.tabs.{srs,drill}` and `review.drill.*`
  - `interview.tabs.{bank,mock}`, `interview.kind.{concept,coding,scenario,system}`, `interview.tip`, and `interview.mock.*`
  - `dashboard.drillWeak` and `dashboard.drillTopic`
- Vietnamese prose MUST address the reader as `"bạn"` (never `"ta"`/`"chúng ta"`).

## Verification Commands
1. `pnpm.cmd --filter web typecheck`
2. `pnpm.cmd --filter web build` (ensure no dev server is running; verifies Next.js static export + ESLint/TS)
3. i18n key parity check via Python one-liner comparing nested keys of `apps/web/messages/en.json` and `vi.json`.
4. Dose Design System static check (`Select-String` for raw `#hex`/`oklch`, `backdrop-blur`, `transition-all` in modified `.tsx` files).
5. Live browser UI verification via `browser` subagent on `/review/`, `/interview/`, and `/` (EN + VI toggle, completing a drill session and a mock interview session).
