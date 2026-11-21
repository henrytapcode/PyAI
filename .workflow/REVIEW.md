VERDICT: APPROVE

## Phase 5 Final Diff Review — Side-by-Side Monaco Code Diff

### 1. Scope Lock (Whitelist / Blacklist & Dependency Freeze)
- **Status:** PASS
- Modified/created source files match the 6 files in `.workflow/SPEC.md` File Whitelist (`apps/web/src/components/code-editor.tsx`, `apps/web/src/components/code-diff-dialog.tsx`, `apps/web/src/components/lesson/exercise-panel.tsx`, `apps/web/src/components/lesson/lesson-view.tsx`, `apps/web/messages/en.json`, `apps/web/messages/vi.json`).
- Zero changes to `package.json`, `pnpm-lock.yaml`, `curriculum/**`, `tools/**`, `storage.ts`, `tokens.css`, or `globals.css`.

### 2. Monaco DiffEditor Safety, Theme Parity, Live Code & Anti-Spoiler Guard
- **Status:** PASS
- **Safe Unmount:** `<DiffEditor>` in `code-diff-dialog.tsx` is conditionally rendered only when `open && activeTarget` is truthy and passes both `keepCurrentOriginalModel` and `keepCurrentModifiedModel` (`true`), preventing Monaco disposed-model exceptions on dialog close.
- **Theme Parity:** `definePyaiThemes` is exported from `code-editor.tsx` and passed to `beforeMount` in both `<Editor>` and `<DiffEditor>` with matching `pyai-dark` / `pyai-light` theme switching.
- **Live Code Wiring:** `lesson-view.tsx` passes `currentCode={exCode}` to `<ExercisePanel />`, and `ExercisePanel` resolves `userCode = currentCode ?? state?.code ?? exercise.starter`.
- **Anti-Spoiler Guard:** Compare buttons (`setDiffTargetId("solution")` and `setDiffTargetId(alt.name)`) render strictly inside the `solutionVisible` branch (`!!state?.solutionViewed || !!state?.passed`).

### 3. Dose Design System Compliance (`apps/web/design.md`)
- **Status:** PASS
- Zero raw color literals (`#hex`, `oklch(`, `rgb(`) in `code-diff-dialog.tsx`, `exercise-panel.tsx`, and `lesson-view.tsx`.
- Zero `backdrop-blur`, zero `transition-all`, zero `font-semibold` / `font-black`.
- `DialogContent` in `code-diff-dialog.tsx` uses `className="max-w-5xl w-[calc(100%-2rem)] gap-0 overflow-hidden p-0"` (no outer `border` class) and header reserves `pr-14` (`sm:pr-14`) for the built-in close button without duplicating it.
- Small interactive pills and mode toggles include `.hit`, `aria-pressed`, and decorative icons carry `aria-hidden="true"`.

### 4. Bilingual EN/VI i18n Parity
- **Status:** PASS
- All 9 new keys under `exercise` (`compare`, `compareShort`, `diffTitle`, `diffDescription`, `yourCode`, `modelSolution`, `sideBySide`, `inlineDiff`, `identicalCode`) have exact 1:1 parity across `en.json` and `vi.json`.
- Vietnamese strings consistently address the learner as `"bạn"`.
