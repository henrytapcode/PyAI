# SPEC: Phase 0 — Environment Setup (`curriculum/phase-00-environment/`)

## Tier & Summary
- **Tier:** **TIER 3 (Strict 5-Phase)** — Creates >60 files across 4 complete bilingual beginner lessons (`p0-01-terminal`, `p0-02-uv-venv`, `p0-03-git`, `p0-04-vscode`), `phase-test.yaml`, and updates `curriculum/syllabus.yaml` & `README.md`.
- **Summary:** Complete the final "Planned / Sắp ra mắt" phase in PyAI Path (`phase-00-environment`, `order: 0`, `skippable_by_placement: true`) so all 9 phases (0–8) and both Capstones are 100% live (`60` lessons, `14` exams), Pyodide-compatible, bilingual EN/VI, and passing all automated validation gates with `0 error(s), 0 warning(s)`.

## Goal & Non-Goals
### Goals
1. Author all 4 bilingual (`en` + `vi`) beginner lessons in `curriculum/phase-00-environment/`:
   - `p0-01-terminal` — Terminal basics (`Terminal cơ bản`)
   - `p0-02-uv-venv` — uv & virtual environments (`uv & môi trường ảo`)
   - `p0-03-git` — Git essentials (`Git căn bản`)
   - `p0-04-vscode` — VS Code for Python (`VS Code cho Python`)
2. Each lesson contains: `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, 2 runnable pure-Python Pyodide examples (`.py`, `.out`, `.en.md`, `.vi.md`), 2 Pyodide exercises (`exercise.yaml`, `prompt.{en,vi}.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_*.{py,en.md,vi.md}`), and `quiz.yaml` (15–16 questions, ≥2 each of `mcq`/`output`/`fill`/`parsons`, 6 flashcards).
3. Author `curriculum/phase-00-environment/phase-test.yaml` (`id: p0-phase-test`, `kind: phase_test`, `phase: p0`, 12 questions, 15 min, pass 0.7).
4. Sync `curriculum/syllabus.yaml` (Phase 0 `outcomes` only) and `README.md` (mark Phase 0 `Available` / `Đã có` in both EN & VI tables).

### Non-Goals (DO NOT TOUCH)
- Do NOT modify Phases 1–8 (`curriculum/phase-01-*`..`phase-08-*`), `curriculum/capstones/**`, `curriculum/exams/**`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml`, `curriculum/glossary.yaml`, or `curriculum/interview/**`.
- Do NOT modify `apps/web/**`, `tools/**`, `packages/**`, `pyproject.toml`, `uv.lock`, `package.json`, `pnpm-lock.yaml`, or `GEMINI.md`.
- Do NOT mark any Phase 0 lesson or exercise as `runner: local`; ALL Phase 0 executable code runs in-browser in Pyodide (pure Python 3.11+ stdlib only; ZERO `subprocess`, `os.system`, real `git`/`uv` binaries, or network calls in Python code blocks, examples, exercises, or quiz code).

## File Whitelist
- `curriculum/phase-00-environment/p0-01-terminal/{meta.yaml,lesson.en.md,lesson.vi.md,quiz.yaml}`
- `curriculum/phase-00-environment/p0-01-terminal/examples/{01_path_navigation,02_cli_args}.{py,out,en.md,vi.md}`
- `curriculum/phase-00-environment/p0-01-terminal/exercises/ex01-path-resolver/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-01-terminal/exercises/ex02-script-runner/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-02-uv-venv/{meta.yaml,lesson.en.md,lesson.vi.md,quiz.yaml}`
- `curriculum/phase-00-environment/p0-02-uv-venv/examples/{01_pyproject_deps,02_venv_isolation}.{py,out,en.md,vi.md}`
- `curriculum/phase-00-environment/p0-02-uv-venv/exercises/ex01-pyproject-inspector/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-02-uv-venv/exercises/ex02-lock-checker/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-03-git/{meta.yaml,lesson.en.md,lesson.vi.md,quiz.yaml}`
- `curriculum/phase-00-environment/p0-03-git/examples/{01_git_lifecycle,02_branch_merge}.{py,out,en.md,vi.md}`
- `curriculum/phase-00-environment/p0-03-git/exercises/ex01-mini-git-status/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-03-git/exercises/ex02-merge-check/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-04-vscode/{meta.yaml,lesson.en.md,lesson.vi.md,quiz.yaml}`
- `curriculum/phase-00-environment/p0-04-vscode/examples/{01_vscode_settings,02_debug_breakpoints}.{py,out,en.md,vi.md}`
- `curriculum/phase-00-environment/p0-04-vscode/exercises/ex01-settings-builder/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/p0-04-vscode/exercises/ex02-debug-trace/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py,alternatives/01_*.{py,en.md,vi.md}}`
- `curriculum/phase-00-environment/phase-test.yaml`
- `curriculum/syllabus.yaml` (ONLY Phase 0 `outcomes` under `id: p0`)
- `README.md` (ONLY Phase 0 status row in EN & VI curriculum tables)

## File Blacklist
- `curriculum/phase-01-python-core/**` .. `curriculum/phase-08-production/**`
- `curriculum/capstones/**`, `curriculum/exams/**`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml`, `curriculum/glossary.yaml`, `curriculum/interview/**`
- `apps/web/**`, `tools/**`, `packages/**`
- `pyproject.toml`, `uv.lock`, `package.json`, `pnpm-lock.yaml`, `.env*`, `GEMINI.md`

## Technical Design & Interface Contracts

### Shared Phase 0 Rules (ALL 4 Lessons & Phase Test)
- **Metadata (`meta.yaml`):** `phase: p0`, `kind: lesson`, `level: beginner`, `review_by: "2027-10-01"`, `duration_min: 10..15`, all `tags` MUST exist in `curriculum/topics.yaml` (`setup`, `files`, `strings`, `packaging`, `git`, `debugging`, `linting`, `json`, `stdlib`, `dicts`, `lists`, `loops`).
- **Pyodide-Safe Teaching Strategy:**
  - Real OS shell / config commands go in non-Python fenced blocks (` ```bash `, ` ```powershell `, ` ```toml `, ` ```json `) showing cross-platform Windows PowerShell + macOS/Linux workflows.
  - All runnable ` ```python ` blocks in `lesson.*.md`, examples, exercises, and quizzes use **pure Python 3.11+ stdlib only** (no `subprocess`, no real filesystem/network side effects, no external packages).
  - Keep lesson Python blocks compact & illustrative so NO `solution.py` shares ≥5 consecutive lines with `lesson.en.md` (`check_solution_overlap` = 0 warnings).
  - Every lesson includes ≥2 visuals (Mermaid diagram + comparison/trace tables), ≥1 **Visualize** prompt on a short (<600 steps) Python block, **Common mistakes**, **Recap**, and **Take it further**.
  - Vietnamese prose addresses the reader as `"bạn"` (never `"ta"`/`"chúng ta"` except `"người ta"`), keeping English technical terms with a Vietnamese gloss on first use; identical code blocks & mermaid line counts between EN/VI.
- **Exercise & Quiz Invariants:**
  - Every exercise: `starter.py` imports cleanly and fails 100% under `EXERCISE_TARGET=starter`; `solution.py` + `alternatives/01_*.py` pass 100% under BOTH `pytest` and `tools/pyrunner/runner.py` (supported pytest subset only); 3 escalating EN/VI hints; `ruff check curriculum` clean.
  - Every `quiz.yaml`: 15–16 questions (`p0-0N-q01`..), ≥2 each of `mcq`, `output`, `fill`, `parsons`; 6 flashcards (`p0-0N-f01`..`f06`); balanced MCQ option lengths; deterministic single-order Parsons; pure Python in `output`/`fill`/`parsons`.

### 1. `p0-01-terminal` (order: 1, prerequisites: `[]`, tags: `[setup, files, strings]`)
- **Lesson scope:** Terminal mental model (cwd, relative vs absolute paths, `.` and `..`), Windows PowerShell vs macOS/Linux (`pwd`, `ls`, `cd`, `mkdir`), running `python script.py` & passing CLI args, exit codes (`0` vs non-zero).
- **Examples:** `01_path_navigation.py` (pure-Python virtual directory navigation with `PurePosixPath`), `02_cli_args.py` (parsing `argv`-style command tokens and exit codes).
- **Exercises:**
  - `ex01-path-resolver` (`p0-01-ex01`, `code`, difficulty 1):
    - `resolve_path(cwd: str, target: str) -> str`: resolves absolute (`/...`) or relative (`src/app.py`, `.`, `..`) POSIX paths against `cwd`, collapsing duplicate slashes and clamping `..` at `"/"`.
    - `split_command(line: str) -> tuple[str, list[str]]`: strips whitespace and splits into `(cmd, args)`; raises `ValueError` on empty/blank input.
  - `ex02-script-runner` (`p0-01-ex02`, `code`, difficulty 2):
    - `find_python_files(entries: list[str], folder: str = "") -> list[str]`: returns sorted `.py` paths under normalized `folder` prefix (empty `folder` matches all `.py` entries).
    - `build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]`: validates `script.strip().endswith(".py")` (else `ValueError`), returns `["uv", "run", "python", script, *args]` or `["python", script, *args]`.

### 2. `p0-02-uv-venv` (order: 2, prerequisites: `[p0-01-terminal]`, tags: `[setup, packaging, stdlib]`)
- **Lesson scope:** Why virtual environments exist (avoiding global Python conflicts), `uv init`, `uv add`, `uv sync`, `uv run python`, reading `pyproject.toml` vs `uv.lock`, `.venv/` isolation and `.gitignore`.
- **Examples:** `01_pyproject_deps.py` (reading a `pyproject.toml` string with stdlib `tomllib`), `02_venv_isolation.py` (comparing two isolated project environments and detecting missing/mismatched packages).
- **Exercises:**
  - `ex01-pyproject-inspector` (`p0-02-ex01`, `code`, difficulty 1):
    - `parse_dependencies(toml_text: str) -> dict[str, str]`: parses `[project].dependencies` via `tomllib.loads` into `{normalized_name_lower: version_spec}` (e.g., `"PyYAML>=6.0"` → `"pyyaml": ">=6.0"`, `"pytest"` → `"pytest": ""`; handles `==`, `>=`, `<=`, `~=`, `!=`, `>`, `<`). Returns `{}` if `[project]` or `dependencies` missing.
    - `missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]`: case-insensitive comparison returning sorted lowercase names present in `required` but absent from `installed`.
  - `ex02-lock-checker` (`p0-02-ex02`, `code`, difficulty 2):
    - `check_venv_isolation(envs: dict[str, dict[str, str]], project: str, package: str, expected_version: str) -> dict`: returns `{"ok": bool, "status": str, "installed": str | None}` with `status` in `{"unknown_env", "missing_package", "version_mismatch", "ok"}`.
    - `diff_lockfiles(old_lock: dict[str, str], new_lock: dict[str, str]) -> dict[str, list[str]]`: returns `{"added": [...], "removed": [...], "changed": [...]}` (all lists sorted ascending).

### 3. `p0-03-git` (order: 3, prerequisites: `[p0-01-terminal]`, tags: `[setup, git, dicts]`)
- **Lesson scope:** Git's 3 areas (Working Tree → Staging Area → Repository), `git status`, `git add`, `git commit`, `.gitignore` hygiene (never committing `.venv/` or `.env`), branching (`git switch -c`, `git merge`), merge conflicts, and `git push` / `git pull` with GitHub.
- **Examples:** `01_git_lifecycle.py` (simulating working tree, staging, and commits with dicts), `02_branch_merge.py` (simulating fast-forward and 3-way merge conflict detection).
- **Exercises:**
  - `ex01-mini-git-status` (`p0-03-ex01`, `code`, difficulty 1):
    - `git_status(committed: dict[str, str], staged: dict[str, str], working: dict[str, str]) -> dict[str, list[str]]`: returns sorted lists for:
      - `"staged"`: paths where `staged.get(p) != committed.get(p)` (added, modified, or deleted in index relative to `committed`),
      - `"untracked"`: paths in `working` not in `committed` and not in `staged`,
      - `"modified"`: paths in `working` that exist in `staged` with `working[p] != staged[p]`,
      - `"deleted"`: paths in `staged` that are absent from `working`.
    - `stage_files(staged: dict[str, str], working: dict[str, str], paths: list[str]) -> dict[str, str]`: returns a **new** staged dict (never mutating input `staged`), updating each path from `working` (or removing from staged if absent from `working` but present in `staged`, else raising `KeyError` if absent from both `working` and `staged`).
  - `ex02-merge-check` (`p0-03-ex02`, `code`, difficulty 2):
    - `three_way_merge(base: dict[str, str], main: dict[str, str], feature: dict[str, str]) -> dict`: merges all keys across `base | main | feature`; if one side equals `base` take the other side (deleting if absent on the changed side); if both sides match keep that value; if both sides changed differently from `base` and from each other record key in sorted `"conflicts"` (keeping `main`'s value if present in `"merged"`). Returns `{"merged": dict[str, str], "conflicts": list[str]}`.
    - `is_valid_commit_msg(msg: str) -> bool`: takes first line (before `\n`), returns `True` iff non-empty after strip, `len(subject) <= 72`, does not end with `"."`, and starts with an ASCII letter.

### 4. `p0-04-vscode` (order: 4, prerequisites: `[p0-02-uv-venv]`, tags: `[setup, debugging, linting, json]`)
- **Lesson scope:** Selecting the `.venv` Python interpreter in VS Code, configuring `.vscode/settings.json` for Ruff format-on-save, running tests from Testing sidebar, using breakpoints, Step Over/Into, Call Stack, and Watch panel in the VS Code Debugger.
- **Examples:** `01_vscode_settings.py` (building and checking `.vscode/settings.json` with `json`), `02_debug_breakpoints.py` (stepping through a loop with a watch-table trace to locate an off-by-one bug).
- **Exercises:**
  - `ex01-settings-builder` (`p0-04-ex01`, `code`, difficulty 1):
    - `build_vscode_settings(venv_path: str, line_length: int = 100, format_on_save: bool = True) -> dict`: raises `ValueError` if `not venv_path.strip()` or not `(40 <= line_length <= 200)`; returns `{"python.defaultInterpreterPath": venv_path.strip(), "editor.formatOnSave": bool(format_on_save), "ruff.lineLength": line_length, "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"}}`.
    - `validate_settings_json(raw_json: str) -> tuple[bool, list[str]]`: parses `raw_json` with `json.loads`; if invalid JSON or top-level is not a `dict`, returns `(False, ["invalid_json"])`; otherwise checks required keys `("python.defaultInterpreterPath", "editor.formatOnSave", "[python]")` (and that `python.defaultInterpreterPath` is a non-empty `str`), returning `(len(errors) == 0, errors)`.
  - `ex02-debug-trace` (`p0-04-ex02`, `debug`, difficulty 2):
    - `find_first_above(values: list[float], threshold: float) -> int | None`: starter contains a realistic off-by-one / `>=` bug; fixed version returns the 0-based index of the first element strictly `> threshold`, or `None` if none exists.
    - `trace_watch(values: list[int], breakpoint_val: int) -> list[dict]`: steps through `values`, keeping a running `running_sum` and recording `{"index": i, "value": v, "running_sum": running_sum, "hit_breakpoint": v == breakpoint_val}` per step, stopping immediately after recording the first step where `hit_breakpoint` is `True`.

### 5. Phase 0 Test (`curriculum/phase-00-environment/phase-test.yaml`)
- `id: p0-phase-test`, `kind: phase_test`, `phase: p0`, `duration_min: 15`, `pass_score: 0.7`, 12 questions (`p0-test-q01`..`q12`): 3 per lesson (`p0-01`..`p0-04`), mix of `mcq`, `output`, `fill`, `parsons` (pure Python stdlib only in code blocks, balanced MCQ lengths, full EN/VI parity).

## Verification Commands
```powershell
# 1. Per-lesson targeted validation, pytest, starter-fail, ruff
uv run python tools/validate.py --path curriculum/phase-00-environment/p0-01-terminal
uv run python tools/validate.py --path curriculum/phase-00-environment/p0-02-uv-venv
uv run python tools/validate.py --path curriculum/phase-00-environment/p0-03-git
uv run python tools/validate.py --path curriculum/phase-00-environment/p0-04-vscode
uv run python tools/validate.py --path curriculum/phase-00-environment
uv run python -m pytest curriculum/phase-00-environment -q
$env:EXERCISE_TARGET='starter'; uv run python -m pytest curriculum/phase-00-environment -q; Remove-Item Env:EXERCISE_TARGET

# 2. Repo-wide QA gates (must all pass with 0 errors AND 0 warnings)
uv run ruff check curriculum
uv run python -m pytest curriculum -q
uv run python -m pytest tools packages -q
uv run python tools/validate.py --fast
pnpm.cmd --filter web typecheck
pnpm.cmd --filter web build
```
