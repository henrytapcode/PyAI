# SPEC: M5 Wave 2B — Resolve All 33 Pre-Existing Phase 1–8 Overlap Warnings

## Tier & Summary
- **Tier:** **TIER 3 (Strict 5-Phase)** — Touches 27 files (>6 files) across Phases 1–8 (`26 solution.py` files + `tasks/M5-PLAN.md`), ZERO protected zones, ZERO public API or test changes.
- **Summary:** Refactor the 26 existing Phase 1–8 `solution.py` files that currently trigger 33 `"N consecutive lines copied from lesson code"` warnings in `tools/validate.py`, bringing repo-wide `uv run python tools/validate.py --fast` to **`OK: 0 error(s), 0 warning(s)`** and completing Milestone M5.

## Goal & Non-Goals
### Goals
1. Eliminate all 33 overlap warnings (`tools.validate.check_solution_overlap`, `min_run=5`) across 26 `solution.py` files in Phases 1–8 through clean, idiomatic, behavior-preserving Python refactors.
2. Keep 100% of existing exercise tests (`test_exercise.py`), browser runner (`tools/pyrunner/runner.py`), `python -W error` (Phase 4+), and `ruff check curriculum` green without modifying any test, starter, lesson, or validator file.
3. Update `tasks/M5-PLAN.md` to mark `7a–7c` (`m5-overlap-*`) and M5 complete.

### Non-Goals (DO NOT TOUCH)
- Do NOT modify any `test_exercise.py`, `starter.py`, `lesson.en.md`, `lesson.vi.md`, `prompt.*.md`, `exercise.yaml`, `quiz.yaml`, `examples/*`, or `alternatives/*`.
- Do NOT modify `tools/validate.py` or weaken `min_run=5` / `_overlap_lines`.
- Do NOT modify `curriculum/capstones/**`, `curriculum/exams/**`, `apps/web/**`, `packages/**`, or any config/lockfiles.
- Do NOT "cheat" by inserting dummy no-op lines, comments, or `# noqa` (note: `_overlap_lines` ignores blank lines, `#` comments, `import` lines, and docstring quotes anyway).

## File Whitelist (27 files — 3 Disjoint Parallel Batches + Final Plan Update)

### Batch A (`T1 [PARALLEL]` — Phases 1–3: 10 files, 14 warnings)
1. `curriculum/phase-01-python-core/p1-06-mini-project/exercises/ex01-report/solution.py` (1 warning)
2. `curriculum/phase-01-python-core/p1-06-mini-project/exercises/ex02-stats/solution.py` (1 warning)
3. `curriculum/phase-02-intermediate/p2-03-inheritance/exercises/ex01-model-family/solution.py` (1 warning)
4. `curriculum/phase-02-intermediate/p2-03-inheritance/exercises/ex02-pipeline/solution.py` (1 warning)
5. `curriculum/phase-02-intermediate/p2-04-dataclasses/exercises/ex02-shared-list/solution.py` (2 warnings)
6. `curriculum/phase-02-intermediate/p2-05-typing/exercises/ex01-annotate-functions/solution.py` (1 warning)
7. `curriculum/phase-02-intermediate/p2-09-mini-project/exercises/ex01-model-and-file/solution.py` (1 warning)
8. `curriculum/phase-02-intermediate/p2-09-mini-project/exercises/ex02-report/solution.py` (1 warning)
9. `curriculum/phase-03-code-quality/p3-05-mini-project/exercises/ex01-config-and-functions/solution.py` (1 warning)
10. `curriculum/phase-03-code-quality/p3-05-mini-project/exercises/ex02-dataset-and-logging/solution.py` (4 warnings)

### Batch B (`T2 [PARALLEL]` — Phases 4–6: 6 files, 7 warnings)
11. `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/solution.py` (1 warning)
12. `curriculum/phase-05-ml/p5-01-math-bridge/exercises/ex02-gradient-descent/solution.py` (1 warning)
13. `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/solution.py` (1 warning)
14. `curriculum/phase-06-deep-learning/p6-01-tensors/exercises/ex02-autograd-descent/solution.py` (1 warning — `runner: local`)
15. `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex02-triage-feedback/solution.py` (1 warning — `runner: local`)
16. `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/solution.py` (2 warnings — `runner: local`)

### Batch C (`T3 [PARALLEL]` — Phases 7–8: 10 files, 12 warnings)
17. `curriculum/phase-07-llm/p7-02-structured-output/exercises/ex01-check-reply/solution.py` (1 warning)
18. `curriculum/phase-07-llm/p7-02-structured-output/exercises/ex02-structured-call/solution.py` (1 warning)
19. `curriculum/phase-07-llm/p7-04-vector-db/exercises/ex02-mini-store/solution.py` (1 warning)
20. `curriculum/phase-07-llm/p7-05-rag/exercises/ex02-answer-with-sources/solution.py` (2 warnings)
21. `curriculum/phase-07-llm/p7-07-agents/exercises/ex02-run-agent/solution.py` (2 warnings)
22. `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/solution.py` (1 warning)
23. `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/solution.py` (1 warning)
24. `curriculum/phase-08-production/p8-01-fastapi/exercises/ex01-notes-routes/solution.py` (1 warning — `runner: local`)
25. `curriculum/phase-08-production/p8-01-fastapi/exercises/ex02-ask-service/solution.py` (1 warning — `runner: local`)
26. `curriculum/phase-08-production/p8-02-docker/exercises/ex01-fix-dockerfile/solution.py` (1 warning)

### Final Status Update (`T4 [SERIAL]`)
27. `tasks/M5-PLAN.md` (update `7a–7c` overlap row & Wave 2A commit hash `75c032e` to mark M5 complete)

## File Blacklist
- ALL `**/test_exercise.py`, `**/starter.py`, `**/lesson.*.md`, `**/prompt.*.md`, `**/exercise.yaml`, `**/quiz.yaml`, `**/alternatives/**`, `**/examples/**`
- `curriculum/capstones/**`, `curriculum/exams/**`, `curriculum/syllabus.yaml`, `curriculum/portfolio.yaml`, `curriculum/topics.yaml`
- `tools/**`, `packages/**`, `apps/web/**`, `pyproject.toml`, `uv.lock`, `package.json`, `pnpm-lock.yaml`, `.env*`, `GEMINI.md`

## Technical Design & Refactoring Rules
1. **How `tools/validate.py` detects overlap (`lines 328–365`):**
   - `_overlap_lines(text)` strips each line and skips blanks, `#` comments, `import`/`from ... import`, and bare `"""`/`'''` lines.
   - `copied_runs(solution, lesson_md, min_run=5)` warns whenever ≥5 consecutive lines in `_overlap_lines(solution)` are all members of the set of lines in `lesson.en.md` Python code blocks.
2. **Approved Idiomatic Refactoring Patterns:**
   - Restructure helper logic cleanly (e.g., extract small focused helper functions, use clear comprehensions/generator expressions, tuple/dict unpacking, explicit local variable names, early returns, or concise f-strings/inline expressions) while preserving exact public signatures, class/field names, return types, and edge-case semantics tested by `test_exercise.py`.
   - For multi-line string literals (SQL in `p4-06/ex02`, Dockerfile in `p8-02/ex01`): assemble cleanly with `"\n".join([...])` or single-line clauses so the resulting string is identical while avoiding raw multi-line copy runs.
   - Keep code pedagogical, concise, and appropriate for the phase's level (e.g., Phase 1 solutions must remain beginner-friendly — no obscure tricks).
3. **Runtime Safety Constraints:**
   - **Phases 1–5, 7, `p8-02` (Pyodide):** Must pass both `pytest` AND `tools/pyrunner/runner.py` (checked automatically by `validate.py --path <lesson_dir>`). Phase 4+ must run clean under `python -W error` (Pyodide `int32` safe).
   - **Phase 6 (`p6-01`, `p6-03`, `p6-04` — `runner: local`):** Preserve `torch.manual_seed(0)`, CPU-only execution, `local_files_only=True`, and cached `REPO`/`REV` constants.
   - **Phase 8 (`p8-01` — `runner: local`, FastAPI `TestClient`):** Preserve exact FastAPI routes/status codes/Pydantic schemas. On Windows, running `p8-01` tests inside the sandbox may hang on loopback sockets; run `p8-01` verification outside sandbox if needed.
4. **Fast Overlap Check Command (runs in ~1 second during iteration):**
   ```powershell
   uv run python -c "import pathlib; from tools import validate; rep = validate.Report(); [validate.check_solution_overlap(rep, p) for p in sorted(pathlib.Path('curriculum').glob('*/*')) if (p / 'lesson.en.md').exists()]; print(f'TOTAL: {len(rep.warnings)}'); print('\n'.join(rep.warnings))"
   ```

## Verification Commands
```powershell
# 1. Instant overlap counter (must print TOTAL: 0)
uv run python -c "import pathlib; from tools import validate; rep = validate.Report(); [validate.check_solution_overlap(rep, p) for p in sorted(pathlib.Path('curriculum').glob('*/*')) if (p / 'lesson.en.md').exists()]; print(f'TOTAL: {len(rep.warnings)}'); print('\n'.join(rep.warnings))"

# 2. Targeted lesson validation & tests per batch
uv run python -m pytest <edited_exercise_dirs> -q
uv run python tools/validate.py --path <edited_lesson_dir>

# 3. Repo-wide final gates (all must pass with 0 errors AND 0 warnings)
uv run ruff check curriculum
uv run python -m pytest curriculum -q
uv run python -m pytest tools packages -q
uv run python tools/validate.py --fast
pnpm.cmd --filter web typecheck
```
