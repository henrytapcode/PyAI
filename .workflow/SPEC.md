# SPEC: M5 Continuation — Web Build Unblock, Capstone 2 (`cap-02-tool-agent`), and Final Mock Exams

## Tier & Summary
- **Tier:** **TIER 3 (Strict 5-Phase)** — Touches >6 files across multiple modules (`apps/web`, `curriculum/capstones`, `curriculum/exams`, shared registries `syllabus.yaml` & `portfolio.yaml`) and includes a production build blocker.
- **Summary:** Resume M5 from checkpoint `dcb33c8`. First unblock the failing `pnpm.cmd --filter web build` (Turbopack PostCSS worker crash on Windows), then build Capstone 2 (`cap-02-tool-agent`) and the two remaining mock exams (`mock-ai-engineer`, `mock-final`).
- **Next Wave (Out of Scope for this SPEC — separate SPEC after Wave 1 Reviewer approval):** PDF exporter (`tools/export_pdf.py`, requires user approval if adding Playwright), 33 pre-existing overlap warnings cleanup (`phases 1–8`), E2E desktop/mobile UI sweep, and final doc updates.

## Goal & Non-Goals
### Goals
1. Diagnose and fix the `pnpm.cmd --filter web build` Turbopack failure on `apps/web/src/app/globals.css` so static export (`apps/web/out/`) succeeds cleanly.
2. Deliver complete Capstone 2 (`curriculum/capstones/cap-02-tool-agent/`) — `meta.yaml`, `lesson.{en,vi}.md`, 3 examples, 3 Pyodide-compatible `project` exercises (with alternatives), and `quiz.yaml` — and link it in `curriculum/syllabus.yaml` and `curriculum/portfolio.yaml`.
3. Deliver `curriculum/exams/mock-ai-engineer.yaml` (24 questions, Phases 6–8) and `curriculum/exams/mock-final.yaml` (40 questions, Phases 1–8 weighted to 5–8), passing full schema, runner, and EN/VI parity validation.

### Non-Goals (DO NOT TOUCH)
- Do NOT modify `curriculum/capstones/cap-01-rag-chatbot/` (already completed, review-fixed, and green).
- Do NOT modify `curriculum/phase-01-*` through `curriculum/phase-08-*` or existing exams (`mock-python-core.yaml`, `mock-data-ml.yaml`).
- Do NOT modify `packages/pyai_llm/`, `tools/schema/*`, `tools/validate.py`, `tools/build_content.py`, `tools/pyrunner/*`, or `tools/localrunner/*`.
- Do NOT install new npm or Python dependencies (e.g., Playwright) or edit lockfiles (`pnpm-lock.yaml`, `uv.lock`, `.env*`).
- Do NOT implement `tools/export_pdf.py` or fix the 33 pre-existing phase 1–8 overlap warnings in this wave.

## File Whitelist
### Wave 1A — Checkpoint Build Blocker Fix (only minimal config/CSS fix if code change is required)
- `apps/web/next.config.ts`
- `apps/web/postcss.config.mjs`
- `apps/web/package.json`
- `apps/web/src/app/globals.css`

### Wave 1B — Capstone 2 (`cap-02-tool-agent`)
- `curriculum/syllabus.yaml` (ONLY the `cap-02-tool-agent` entry under `capstones:`)
- `curriculum/portfolio.yaml` (ONLY the `cap-tool-agent` entry under `projects:`)
- `curriculum/capstones/cap-02-tool-agent/meta.yaml`
- `curriculum/capstones/cap-02-tool-agent/lesson.en.md`
- `curriculum/capstones/cap-02-tool-agent/lesson.vi.md`
- `curriculum/capstones/cap-02-tool-agent/examples/01_scoped_tools.{py,out,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/examples/02_retry_budget.{py,out,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/examples/03_trace_summary.{py,out,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex01-scoped-permissions/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex01-scoped-permissions/alternatives/01_*.{py,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex02-retry-budget/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex02-retry-budget/alternatives/01_*.{py,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex03-trace-report/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `curriculum/capstones/cap-02-tool-agent/exercises/ex03-trace-report/alternatives/01_*.{py,en.md,vi.md}`
- `curriculum/capstones/cap-02-tool-agent/quiz.yaml`

### Wave 1C — Mock Exams
- `curriculum/exams/mock-ai-engineer.yaml`
- `curriculum/exams/mock-final.yaml`

## File Blacklist
- `curriculum/capstones/cap-01-rag-chatbot/**`
- `curriculum/phase-01-python-core/**` .. `curriculum/phase-08-production/**`
- `curriculum/exams/mock-python-core.yaml`, `curriculum/exams/mock-data-ml.yaml`
- `curriculum/topics.yaml`, `curriculum/glossary.yaml`, `curriculum/interview/**`
- `packages/pyai_llm/**`
- `tools/**`
- `apps/web/src/lib/**`, `apps/web/src/components/**`, `apps/web/messages/**`, `apps/web/src/app/tokens.css`
- `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock`, `.env*`, `GEMINI.md`, `CLAUDE.md`

## Technical Design & Interface Contracts

### 1. Web Build Blocker (`T1`)
- **Observed failure at checkpoint `dcb33c8`:** `pnpm.cmd --filter web build` fails during Next.js 16.4.5 Turbopack build with `TurbopackInternalError: Failed to write app endpoint /_not-found/page` caused by `[project]/apps/web/src/app/globals.css [app-client] (css) -> creating new process -> node process exited before we could connect to it with exit code: 0`. Also `NODE_EXTRA_CA_CERTS` points to a missing file (`9router/mitm/rootCA.crt`).
- **Fix contract:** Identify root cause (stale `.next` cache, Turbopack PostCSS child-process crash on Windows, or `NODE_EXTRA_CA_CERTS`). Keep static export (`output: "export"`, `apps/web/out/`) intact, preserve Tailwind v4 & Dose tokens (`tokens.css` untouched), and do not weaken TypeScript/build checks.

### 2. Capstone 2 (`cap-02-tool-agent`) — Must NOT duplicate `p7-10-mini-project-agent`
- **Metadata (`meta.yaml` & `syllabus.yaml`):**
  - `id: cap-02-tool-agent`, `phase: cap`, `order: 2`, `kind: project`, `level: applied`, `duration_min: 90`, `review_by: "2027-05-01"`.
  - `prerequisites: [p7-07-agents, p7-10-mini-project-agent, p8-04-monitoring]`.
  - `tags: [llm, agents, production, logging]` (all in `curriculum/topics.yaml`).
  - No `runner: local` (lesson + all 3 exercises run cleanly in Pyodide).
- **Exercise 1 (`cap-02-ex01`, `ex01-scoped-permissions`):**
  - Data types:
    - `ToolSpec(name: str, fn: Callable, required_args: tuple[str, ...], risk: str, max_amount: float | None = None)` where `risk in ("read", "write", "destructive")`.
    - `RequestContext(request_id: str, role: str, allowed_tools: frozenset[str] | set[str], confirmation_token: str | None = None)`.
  - `ScopedRegistry`:
    - `register(spec: ToolSpec) -> None`: raises `ValueError` on duplicate `spec.name` or invalid `spec.risk`.
    - `execute(name: str, args: dict, ctx: RequestContext, confirm_fn: Callable[[str, str, dict, str], bool] | None = None) -> dict`:
      - Returns `{"ok": bool, "status": str, "result": Any, "error": str | None}`.
      - Status priority: `"unknown_tool"` → `"denied_scope"` (`name not in ctx.allowed_tools`) → `"invalid_args"` (missing required arg; extra args dropped before calling `fn`) → `"denied_policy"` (`risk == "write"` and `spec.max_amount is not None` and `args.get("amount", 0) > spec.max_amount`) → `"needs_confirmation"` (`risk == "destructive"` and empty/None `ctx.confirmation_token` or `confirm_fn is None`) → `"denied_confirmation"` (`confirm_fn(...)` returns falsy) → `"ok"` / `"tool_error"`.
      - Appends `{"request_id": ctx.request_id, "role": ctx.role, "tool": name, "risk": spec_risk_or_unknown, "status": status}` to `self.audit_log` on EVERY call. Never calls `fn` on any denial.
- **Exercise 2 (`cap-02-ex02`, `ex02-retry-budget`):**
  - Uses standard `FakeClock` (`self.t`, `__call__()`, `advance(seconds)`) and `from pyai_llm import FakeLLM, RateLimitError, Usage`.
  - `Pricing(input_per_1k: float, output_per_1k: float)` and `CostBudget(max_tokens: int, max_cost_usd: float)`:
    - Validates `max_tokens > 0` and `max_cost_usd > 0` (`ValueError`).
    - `record(usage: Usage) -> None` updates `total_tokens` and `cost_usd`; `check() -> str | None` returns `"token_budget"`, `"cost_budget"`, or `None`.
  - `call_with_retry(fn, clock, max_retries: int = 3, base_delay: float = 0.5, idempotent: bool = True) -> dict`:
    - Retries only `(RateLimitError, TimeoutError)` when `idempotent=True`.
    - If `idempotent=False`, executes `fn` at most once (never retries side-effect calls).
    - Advances `clock.advance(base_delay * (2 ** attempt))` between retries (`attempt = 0, 1, ...`).
    - Returns `{"ok": bool, "value": Any, "error": str | None, "attempts": int, "wait_seconds": float}`.
  - `run_budgeted_agent(task, client, registry, ctx, clock, pricing, budget, max_steps=5, max_retries=2) -> dict`:
    - Wraps `client.chat(...)` in `call_with_retry(..., idempotent=True)`; checks `budget.check()` before each step and after recording `resp.usage`.
    - Returns `{"answer": str | None, "stopped_reason": str, "steps": int, "total_tokens": int, "cost_usd": float, "retries": int}` with `stopped_reason in {"final", "max_steps", "token_budget", "cost_budget", "rate_limit"}`.
- **Exercise 3 (`cap-02-ex03`, `ex03-trace-report`):**
  - `TraceRecorder(clock)`:
    - `record_step(request_id: str, step: int, kind: str, name: str, fn: Callable, tokens: int = 0, cost_usd: float = 0.0, retries: int = 0) -> tuple[Any, dict]`: captures `started_at = clock()`, calls `fn()`, computes `duration_ms = round((clock() - started_at) * 1000.0, 3)`, records span `{"request_id", "step", "kind", "name", "status", "started_at", "duration_ms", "tokens", "cost_usd", "retries", "error"}` (`status` = `"ok"` or `"error"`).
    - `to_jsonl() -> str`: newline-joined `json.dumps(span, sort_keys=True)`.
  - `summarize_traces(spans: list[dict], budget_usd: float | None = None) -> dict`:
    - Returns `{"total_requests": int, "total_steps": int, "tool_counts": dict[str, int], "status_counts": dict[str, int], "total_retries": int, "total_tokens": int, "total_cost_usd": float, "p95_step_ms": float, "budget_utilization": float | None, "failed_requests": list[str]}` (nearest-rank p95, rounded 6 decimals for USD, sorted `failed_requests`).
  - `format_report(summary: dict) -> str`: deterministic human-readable report, every line `< 60` chars.
- **Content & Parity Rules (all capstone files & exams):**
  - Every exercise: starter imports cleanly and fails 100% of tests (`EXERCISE_TARGET=starter`), solution + ≥1 alternative pass 100% (pytest + browser runner), 0 lines copied verbatim ≥5 consecutive lines from `lesson.*.md`, 3 escalating hints EN/VI, browser-runner pytest subset only.
  - Vietnamese prose: address reader as `"bạn"` (never `"ta"` / `"chúng ta"` except `"người ta"`), keep English technical terms with Vietnamese gloss on first use, identical code blocks between EN/VI (comments may differ, `# output` comments unchanged), same mermaid line count.
  - Quiz (`cap-02-tool-agent/quiz.yaml`): 15–18 questions (`cap-02-q01`..), ≥2 each of `mcq`, `output`, `fill`, `parsons`; 6 flashcards (`cap-02-f01`..`f06`); balanced MCQ option lengths (correct option never uniquely longest by >20%); Pyodide-only code; Parsons single valid order.

### 3. Mock Exams (`T8`, `T9`)
- **`curriculum/exams/mock-ai-engineer.yaml`:** `id: mock-ai-engineer`, `kind: mock`, `duration_min: 35`, `pass_score: 0.8`, 24 questions (`mock3-q01`..`mock3-q24`) across Phases 6–8 (6 DL/PyTorch/HF, 10 LLM/RAG/Agents/Evals, 8 FastAPI/Docker/Cache/Monitoring).
- **`curriculum/exams/mock-final.yaml`:** `id: mock-final`, `kind: mock`, `duration_min: 60`, `pass_score: 0.8`, 40 questions (`final-q01`..`final-q40`) across Phases 1–8 weighted toward Phases 5–8 (8 P1–P3, 4 P4, 6 P5, 6 P6, 10 P7, 6 P8).
- Both conform to `tools/schema/exam.schema.json`, use valid tags from `curriculum/topics.yaml`, have balanced MCQ lengths, deterministic single-order Parsons, and full EN+VI parity.

## Verification Commands
```powershell
# 1. Targeted validation & tests (run after each task)
uv run python tools/validate.py --path curriculum/capstones/cap-02-tool-agent
uv run python -m pytest curriculum/capstones/cap-02-tool-agent -q
$env:EXERCISE_TARGET='starter'; uv run python -m pytest curriculum/capstones/cap-02-tool-agent -q; Remove-Item Env:EXERCISE_TARGET
uv run python tools/validate.py --path curriculum/exams/mock-ai-engineer.yaml
uv run python tools/validate.py --path curriculum/exams/mock-final.yaml

# 2. Repo-wide gates (must all pass before Reviewer approval)
uv run ruff check curriculum
uv run python -m pytest curriculum -q
uv run python -m pytest tools packages -q
uv run python tools/validate.py --fast
pnpm.cmd --filter web typecheck
pnpm.cmd --filter web build
```
