# Project Profile: python-ai-platform

## Stack & Scale
- **Scale:** Large (monorepo: 60 web src files, 26 tool files, 8 package files, 1,991 curriculum files; 60 lessons across Phases 0–8 + 2 Capstones, 14 exams, 122 exercises).
- **Content & Tooling:** Python >=3.11 managed by `uv` (`pyproject.toml`, `uv.lock`); YAML + Markdown + Python curriculum validated by `jsonschema`, `pytest`, `ruff`; local package `packages/pyai_llm` (deterministic `FakeLLM`).
- **Web App (`apps/web`):** Next.js 16.4.5 (App Router, static export `output: "export"`), React 19, TypeScript 5.9, Tailwind CSS v4, Radix UI, Zustand, `next-intl` (client-side EN/VI), Monaco Editor, Pyodide Web Worker (`public/pyodide-worker.js`). Managed by `pnpm@10.34.7`.
- **Execution Modes:** Pyodide in-browser (phases 0–5, 7, most capstones) + FastAPI local runner (`127.0.0.1:8765`, `tools/localrunner/serve.py`) for `runner: local` lessons/exercises (PyTorch/HF/FastAPI `TestClient`).

## Exact Verification Commands
> Windows PowerShell note: use `pnpm.cmd` (PowerShell blocks `pnpm.ps1`), and always use `uv run python -m pytest` (never `uv run pytest`). Stop any running dev server before `web build`.

- **Install:**
  - Python: `uv sync`
  - Node: `pnpm.cmd install --frozen-lockfile`
  - HF offline cache (for phase 6): `uv run python tools/localrunner/fetch_models.py --check`
- **Lint / Content Validate:**
  - Single-path Python lint (fast): `uv run ruff check <path/to/file-or-dir>`
  - Full curriculum lint: `uv run ruff check curriculum`
  - Targeted lesson/exam validate (fast, seconds): `uv run python tools/validate.py --path <curriculum/path>`
  - Full fast validate (~3–4 min, QA gate only): `uv run python tools/validate.py --fast`
  - Full strict validate (CI gate only): `uv run python tools/validate.py`
- **Typecheck:**
  - `pnpm.cmd --filter web typecheck` (runs `build_content.py` + `tsc --noEmit`)
- **Unit / Targeted Tests (ALWAYS run targeted first; reserve full suite for final QA):**
  - Single test function (fastest): `uv run python -m pytest <path/to/test_file.py> -k <test_name> -q`
  - Single test file: `uv run python -m pytest <path/to/test_exercise.py> -q`
  - Single lesson dir: `uv run python -m pytest curriculum/<phase-or-cap>/<lesson-id> -q`
  - Verify starter fails (PowerShell): `$env:EXERCISE_TARGET='starter'; uv run python -m pytest <exercise-dir> -q; Remove-Item Env:EXERCISE_TARGET`
  - Tools & packages: `uv run python -m pytest tools packages -q`
  - All curriculum tests (~30s, QA gate): `uv run python -m pytest curriculum -q`
- **Build:**
  - Content JSON only: `uv run python tools/build_content.py`
  - Full web static build: `pnpm.cmd --filter web build` (writes `apps/web/out/`; fetches Google Fonts at build time)

## Sensitive / Core Paths (Protected Zones)
- `tools/schema/*.schema.json`, `tools/validate.py`, `tools/build_content.py` — content schema, parity & build pipeline.
- `tools/pyrunner/`, `tools/localrunner/` — browser test runner/tracer & isolated local execution server.
- `packages/pyai_llm/` — deterministic fake LLM contract shared by phases 7–8 and capstones.
- `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml` — shared curriculum registries.
- `apps/web/src/lib/storage.ts`, `apps/web/src/lib/types.ts`, `apps/web/src/lib/content*.ts`, `apps/web/messages/{en,vi}.json` — persistence adapter, data contracts, i18n parity.
- `apps/web/src/app/tokens.css`, `apps/web/src/app/globals.css`, `apps/web/design.md` — Dose design system tokens & a11y rules.
