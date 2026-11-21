# TASKS: Side-by-Side Monaco Code Diff

- [x] T1 [PARALLEL] (Files: `apps/web/src/components/code-editor.tsx`, `apps/web/src/components/code-diff-dialog.tsx`): Export `definePyaiThemes` from `code-editor.tsx`; create Dose-compliant `<CodeDiffDialog />` wrapping `@monaco-editor/react`'s `DiffEditor` with target switcher, side-by-side/inline toggle, identical-code badge, safe unmount props, and load-into-editor footer action per SPEC.md.
- [x] T2 [PARALLEL] (Files: `apps/web/messages/en.json`, `apps/web/messages/vi.json`): Add the 9 new `exercise.*` i18n keys (`compare`, `compareShort`, `diffTitle`, `diffDescription`, `yourCode`, `modelSolution`, `sideBySide`, `inlineDiff`, `identicalCode`) with 1:1 parity in both files.
- [x] T3 [PARALLEL] (Files: `apps/web/src/components/lesson/exercise-panel.tsx`, `apps/web/src/components/lesson/lesson-view.tsx`): Pass `currentCode={exCode}` from `lesson-view.tsx` to `ExercisePanel`; wire `<CodeDiffDialog />` and `Compare` buttons for both main solution and each alternative when `solutionVisible` is true.
- [x] T4 [SERIAL] (QA Gate — Boss): Verified `pnpm.cmd --filter web typecheck` (0 errors), Dose static grep check (0 violations), and `pnpm.cmd --filter web build` (static export).
- [x] T5 [SERIAL] (Reviewer — Argon): Audited `git diff` against `.workflow/SPEC.md` and `apps/web/design.md` -> `.workflow/REVIEW.md` (`VERDICT: APPROVE`).
