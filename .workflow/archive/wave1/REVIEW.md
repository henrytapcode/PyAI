# VERDICT: APPROVE

## 1. Audited Scope & Verification Results

### Scope Lock & Git Diff Hygiene
- **Git Status & Diff (`git status --short`, `git diff --stat`):**
  - Wave 1 changes are strictly confined to the whitelisted files in `.workflow/SPEC.md`:
    - `apps/web/package.json` (only the `"build"` script line updated)
    - `curriculum/syllabus.yaml` (only the `cap-02-tool-agent` entry under `capstones:` updated)
    - `curriculum/portfolio.yaml` (only the `cap-tool-agent` entry under `projects:` updated)
    - `curriculum/capstones/cap-02-tool-agent/**` (new lesson, 3 examples, 3 exercises with alternatives, and `quiz.yaml`)
    - `curriculum/exams/mock-ai-engineer.yaml` and `curriculum/exams/mock-final.yaml` (new mock exams)
  - Zero `File Blacklist` files, lockfiles (`pnpm-lock.yaml`, `uv.lock`), `apps/web/src/app/layout.tsx`, `apps/web/src/app/tokens.css`, `curriculum/capstones/cap-01-rag-chatbot/**`, or Phase 1–8 files were touched.
  - All `T1`–`T10` tasks in `.workflow/TASKS.md` are marked `[x]`, and the Wave 2 Backlog (`W2-1`..`W2-3`) remains untouched.

### Audit Against `.workflow/SPEC.md` & `.workflow/CRITIQUE.md`
1. **Web Build Fix (`T1` — `apps/web/package.json`):**
   - Cross-platform inline Node wrapper deletes `env.NODE_EXTRA_CA_CERTS` only when the referenced file does not exist on disk (`!fs.existsSync(env.NODE_EXTRA_CA_CERTS)`), preserving Linux CI compatibility while fixing the Windows TLS font-fetch failure after clearing stale `.next/`.
   - No TypeScript or Next.js build checks were weakened; `apps/web/out/index.html` and `apps/web/out/lesson/cap-02-tool-agent/index.html` are present in the static export output.
2. **Capstone 2 (`curriculum/capstones/cap-02-tool-agent/`):**
   - **Metadata & Bilingual Lesson (`meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `syllabus.yaml`, `portfolio.yaml`):** Matches all SPEC contracts (`id: cap-02-tool-agent`, `phase: cap`, `order: 2`, `kind: project`, `level: applied`, `duration_min: 90`, `prerequisites: [p7-07-agents, p7-10-mini-project-agent, p8-04-monitoring]`, `tags: [llm, agents, production, logging]`). Exact EN/VI line parity (188 lines each), matching Mermaid diagram and Markdown tables, 1 Visualize prompt, reader addressed as `"bạn"` (zero `"ta"`/`"chúng ta"`), and compact illustrative code blocks with zero lesson-copy overlap warnings.
   - **Examples (`examples/01_scoped_tools.*`, `02_retry_budget.*`, `03_trace_summary.*`):** All 3 examples match their `.out` files and follow the 4-section EN/VI markdown structure.
   - **Exercise 1 (`ex01-scoped-permissions`):** `ToolSpec`, `RequestContext`, and `ScopedRegistry` enforce strict status priority (`"unknown_tool"` -> `"denied_scope"` -> `"invalid_args"` -> `"denied_policy"` -> `"needs_confirmation"` -> `"denied_confirmation"` -> `"ok"` / `"tool_error"`), reject `None`/`bool`/non-numeric `"amount"` values when `max_amount is not None` on `"write"` tools (handling `max_amount=0.0` via `is not None`), filter unknown arguments before `confirm_fn` and `spec.fn`, and log every call (including `risk="unknown"` on unknown tools) to `self.audit_log`.
   - **Exercise 2 (`ex02-retry-budget`):** Completely self-contained (zero imports from `ex01`), implements `Pricing` (`>= 0` validation), `CostBudget.record(usage, pricing) -> float` and `check()`, `call_with_retry` (`idempotent=False` runs at most once; retries `(RateLimitError, TimeoutError)` with `clock.advance(base_delay * (2 ** attempt))`), and duck-typed `run_budgeted_agent` with `tools` parameter, pre/post-step budget checks, `{"role": "assistant", "content": resp.content or ""}`, and single-shot tool execution.
   - **Exercise 3 (`ex03-trace-report`):** Implements `TraceRecorder` (`record_step` catching `Exception` into `status="error"` + `to_jsonl()`), `summarize_traces` (empty spans `p95_step_ms = 0.0`, `kind == "tool"` filtering for `tool_counts`, nearest-rank `p95_step_ms`, `budget_utilization = None` when `budget_usd is None or budget_usd <= 0`, sorted unique `failed_requests`), and `format_report` with every line `< 60` characters.
   - **Quiz (`quiz.yaml`):** 16 questions (`cap-02-q01`..`q16`: 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons`) and 6 flashcards (`cap-02-f01`..`f06`), balanced MCQ option lengths, deterministic single-order Parsons, full EN/VI parity.
3. **Mock Exams (`curriculum/exams/mock-ai-engineer.yaml`, `mock-final.yaml`):**
   - `mock-ai-engineer.yaml`: 24 questions (`mock3-q01`..`q24`, `duration_min: 35`, `pass_score: 0.8`) across Phases 6–8 (6 DL/PyTorch/HF, 10 LLM/RAG/Agents/Evals, 8 FastAPI/Docker/Cache/Monitoring).
   - `mock-final.yaml`: 40 questions (`final-q01`..`q40`, `duration_min: 60`, `pass_score: 0.8`) across Phases 1–8 weighted toward Phases 5–8 (8 P1–P3, 4 P4, 6 P5, 6 P6, 10 P7, 6 P8).
   - All executable `output`/`fill`/`parsons` blocks use pure Python / `numpy` / `sqlite3` / `pyai_llm` (zero `torch`, `transformers`, `fastapi`, or `uvicorn` imports).

### Verification Command Outputs
- `uv run ruff check curriculum` → **PASS** (`All checks passed!`)
- `uv run python tools/validate.py --path curriculum/capstones/cap-02-tool-agent` → **PASS** (`OK: 0 error(s), 0 warning(s). Checked 1 lessons, 10 markdown pairs, 3 examples, 12 lesson output blocks, 3 alternatives, 3 exercises, 16 questions.`)
- `uv run python tools/validate.py --path curriculum/exams` → **PASS** (`OK: 0 error(s), 0 warning(s). Checked 108 questions, 4 exams.`)
- `uv run python -m pytest curriculum/capstones/cap-02-tool-agent -q` → **PASS** (`34 passed`)
- `$env:EXERCISE_TARGET='starter'; uv run python -m pytest curriculum/capstones/cap-02-tool-agent -q; Remove-Item Env:EXERCISE_TARGET` → **PASS** (`34 failed` — 100% starter failure verified)
- `pnpm.cmd --filter web typecheck` → **PASS** (`Built 56 lessons, 13 exams, 336 flashcards, 898 questions -> apps\web\src\generated`, `tsc --noEmit` exited `0`)

---

## 2. Findings

### `[BLOCKER]`
- None.

### `[MINOR]`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex03-trace-report/starter.py:1-2`: Uses `# noqa: F401` on `import json` and `import math` in the starter template so unused imports pass `ruff` before the learner fills in the methods. This is benign and standard for starter templates, noted here for completeness.
