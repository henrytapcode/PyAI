# SPEC: Side-by-Side Monaco Code Diff

## Tier & Summary
- **Tier:** **TIER 2** (touches 6 files within `apps/web`: `code-editor.tsx`, new `code-diff-dialog.tsx`, `exercise-panel.tsx`, `lesson-view.tsx`, and `messages/{en,vi}.json`; zero new dependencies, zero backend/schema changes).
- **Summary:** Add a Dose-compliant Side-by-Side Monaco `DiffEditor` modal allowing learners to visually compare their live exercise code against `solution.py` and any `alternatives/*.py` once the solution is visible (passed or unlocked & viewed), with desktop side-by-side / mobile inline toggle and one-click load into editor.

## Goal & Non-Goals
### Goal
1. Export shared `definePyaiThemes` from `apps/web/src/components/code-editor.tsx` so both `Editor` and `DiffEditor` share identical Dose `pyai-light` / `pyai-dark` Monaco themes.
2. Create `apps/web/src/components/code-diff-dialog.tsx` wrapping `@monaco-editor/react`'s `DiffEditor` inside Radix `DialogContent`, supporting:
   - Live comparison (`original = userCode`, `modified = selectedTarget.code`), read-only on both sides.
   - Instant target switching between `Model solution` and all `exercise.alternatives` inside the modal.
   - Responsive Side-by-Side (`>= 768px` default) vs Inline (`< 768px` default) mode with manual toggle.
   - Identical-code notice badge when `userCode.trim() === target.code.trim()`.
   - Safe unmount without Monaco disposed-model exceptions (`keepCurrentOriginalModel` + `keepCurrentModifiedModel`).
   - One-click `Load into editor` action.
3. Pass live `currentCode={exCode}` from `lesson-view.tsx` into `ExercisePanel`, and expose `Compare with your code` buttons for the main solution and each alternative when `solutionVisible` is true.
4. Maintain 100% EN/VI i18n parity in `apps/web/messages/{en,vi}.json` and full Dose Design System compliance.

### Non-Goals
- Do NOT install any npm or Python packages (Dependency Freeze — `DiffEditor` is already in `@monaco-editor/react@4.7.0`).
- Do NOT modify `curriculum/`, `tools/`, `apps/web/src/lib/storage.ts`, `tokens.css`, or `globals.css`.
- Do NOT allow comparing/viewing solutions before `solutionVisible` is true (preserve anti-spoiler lock).

## File Whitelist
- `apps/web/src/components/code-editor.tsx` (modify)
- `apps/web/src/components/code-diff-dialog.tsx` (create)
- `apps/web/src/components/lesson/exercise-panel.tsx` (modify)
- `apps/web/src/components/lesson/lesson-view.tsx` (modify)
- `apps/web/messages/en.json` (modify)
- `apps/web/messages/vi.json` (modify)

## File Blacklist
- `curriculum/**`, `tools/**`, `packages/**`
- `package.json`, `pnpm-lock.yaml`, `apps/web/package.json`
- `apps/web/src/lib/storage.ts`, `apps/web/src/app/tokens.css`, `apps/web/src/app/globals.css`
- `.env*`

## Technical Design & Interface Contracts

### 1. Shared Theme Export (`apps/web/src/components/code-editor.tsx`)
- Rename `const defineThemes: BeforeMount` → `export const definePyaiThemes: BeforeMount` and pass `beforeMount={definePyaiThemes}` to `<Editor />`. No behavior changes to `CodeEditor`.

### 2. Code Diff Dialog (`apps/web/src/components/code-diff-dialog.tsx`)
Exports:
```ts
export interface DiffTarget {
  id: string;
  label: string;
  code: string;
}

export interface CodeDiffDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  exerciseTitle: string;
  userCode: string;
  targets: DiffTarget[];
  initialTargetId?: string;
  onLoadTarget?: (code: string) => void;
}

export function CodeDiffDialog(props: CodeDiffDialogProps): React.JSX.Element
```
Behavior & Dose rules:
- Uses `Dialog`, `DialogContent`, `DialogTitle`, `DialogDescription` from `@/components/ui/dialog` with `className="max-w-5xl w-[calc(100%-2rem)] gap-0 overflow-hidden p-0"` (NO outer `border` class).
- Header reserves `pr-14` for `DialogContent`'s built-in top-right close button (do NOT render a duplicate close button).
- Tracks `selectedId` state synced with `initialTargetId` whenever `open` transitions to `true` or `initialTargetId` changes; falls back to `targets[0]?.id`.
- Tracks `sideBySide` boolean initialized via `window.matchMedia("(min-width: 768px)").matches` inside `useEffect` (default `true` on desktop, `false` on mobile) and toggleable via two buttons (`sideBySide` / `inlineDiff`, `aria-pressed`, `.hit`).
- When `targets.length > 1`, renders horizontal scrollable target switcher pills (`aria-pressed`, `.hit`).
- When `sideBySide` is true, shows a compact 2-column label bar above the editor: Left = `t("yourCode")`, Right = `activeTarget.label`.
- When `userCode.trim() === activeTarget.code.trim()`, shows a `Badge variant="success"` with `t("identicalCode")`.
- Renders `<DiffEditor>` from `@monaco-editor/react` ONLY when `open` is true, inside a responsive container (`h-[60vh] min-h-[320px] max-h-[680px]`):
  - `language="python"`
  - `original={userCode}`
  - `modified={activeTarget.code}`
  - `beforeMount={definePyaiThemes}`
  - `theme={resolvedTheme === "dark" ? "pyai-dark" : "pyai-light"}`
  - `keepCurrentOriginalModel` and `keepCurrentModifiedModel` both `true` (prevents Monaco disposed-model error on dialog close)
  - `options`: `{ readOnly: true, originalEditable: false, renderSideBySide: sideBySide, minimap: { enabled: false }, scrollBeyondLastLine: false, automaticLayout: true, fontSize: 14, fontFamily: "var(--font-mono-face), 'JetBrains Mono', Consolas, monospace", fontLigatures: true, wordWrap: "on", padding: { top: 12, bottom: 12 }, overviewRulerLanes: 0, scrollbar: { verticalScrollbarSize: 8, horizontalScrollbarSize: 8 } }`
- Footer bar with optional `Load into editor` button (`onLoadTarget(activeTarget.code); onOpenChange(false)`).
- Strict Dose compliance: zero raw color literals (`#hex`, `oklch(`, `rgb(`), zero `backdrop-blur`, zero `transition-all`, zero `font-semibold`/`font-black`, `.hit` on small controls, `aria-hidden="true"` on decorative icons.

### 3. Wiring (`exercise-panel.tsx` & `lesson-view.tsx`)
- `apps/web/src/components/lesson/lesson-view.tsx`: pass `currentCode={exCode}` to `<ExercisePanel />`.
- `apps/web/src/components/lesson/exercise-panel.tsx`:
  - Update props: `{ exercise: Exercise; currentCode?: string; onLoadCode: (code: string) => void }`.
  - Compute `userCode = currentCode ?? state?.code ?? exercise.starter`.
  - Build `diffTargets: DiffTarget[]` (`[{ id: "solution", label: t("modelSolution"), code: exercise.solution }, ...exercise.alternatives.map(alt => ({ id: alt.name, label: loc.t(alt.title) || alt.name, code: alt.code }))]`).
  - Maintain `diffTargetId: string | null` state (`open = diffTargetId !== null`).
  - In `solutionVisible` block:
    - Next to `Load into editor` button under main solution, add `<Button variant="outline" size="sm" onClick={() => setDiffTargetId("solution")}><GitCompareArrows aria-hidden="true" /> {t("compare")}</Button>`.
    - Under each alternative's `<StaticCode code={alt.code} />`, add a compact button row with `Compare` (`setDiffTargetId(alt.name)`) and `Load into editor` (`onLoadCode(alt.code)`).
  - Render `<CodeDiffDialog open={diffTargetId !== null} onOpenChange={(o) => !o && setDiffTargetId(null)} exerciseTitle={loc.t(exercise.title)} userCode={userCode} targets={diffTargets} initialTargetId={diffTargetId ?? "solution"} onLoadTarget={onLoadCode} />`.

### 4. i18n Keys (`apps/web/messages/en.json` & `apps/web/messages/vi.json`)
Add under `"exercise"` in BOTH files (exact 1:1 parity, VI uses `"bạn"`):
- `compare`: `"Compare with your code"` / `"So sánh với code của bạn"`
- `compareShort`: `"Compare"` / `"So sánh"`
- `diffTitle`: `"Compare code"` / `"So sánh code"`
- `diffDescription`: `"Compare your code side-by-side with the model solution."` / `"So sánh trực tiếp code của bạn với lời giải mẫu."`
- `yourCode`: `"Your code"` / `"Code của bạn"`
- `modelSolution`: `"Model solution"` / `"Lời giải mẫu"`
- `sideBySide`: `"Side by side"` / `"Song song"`
- `inlineDiff`: `"Inline"` / `"Gộp dòng"`
- `identicalCode`: `"Your code matches this solution."` / `"Code của bạn giống hệt lời giải này."`

## Verification Commands
1. `pnpm.cmd --filter web typecheck`
2. `pnpm.cmd --filter web build`
3. Dose static grep check on `code-diff-dialog.tsx`, `exercise-panel.tsx`, `lesson-view.tsx`: zero `#hex`/`oklch`/`rgb(`, zero `backdrop-blur`, zero `transition-all`, zero `font-semibold`/`font-black`.
