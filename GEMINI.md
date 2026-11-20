# ADAPTIVE ENGINEERING OPERATING SYSTEM

Communicate with the user in Vietnamese. Keep code, technical specs, comments, and commit messages in English.

## 0. Auto-Detect Bootstrap (First Run Only)
- Before planning or editing code, check if `.workflow/PROJECT_PROFILE.md` exists.
- If missing, immediately invoke skill `auto-bootstrap` (read-only scan) to detect the tech stack, repo scale, exact lint/typecheck/test/build commands, and sensitive paths, then save to `.workflow/PROJECT_PROFILE.md`.

## 1. Adaptive Complexity Triage (Auto-Adjust Rigor)
Evaluate every new user request and explicitly declare its Tier before acting:
- **TIER 1 (Fast Track):** Touches 1–2 files, isolated bugfix/UI/script, ZERO protected zones, no public API/schema change.
  - *Flow:* Execute directly (ideal for Neon Orchestrator or single Worker pass). Skip `.workflow/SPEC.md`, but MUST still run Verification Commands before finishing.
- **TIER 2 (Standard):** Touches 3–6 files within 1 module, moderate new feature or refactor.
  - *Flow:* Invoke `spec-and-triage` to write compact `.workflow/SPEC.md` & `.workflow/TASKS.md` → Worker executes strictly inside Whitelist → Deterministic QA → Quick Diff Check.
- **TIER 3 (Strict 5-Phase):** Touches more than 6 files, cross-module architecture, high risk, OR touches ANY protected zone (DB/Auth/Payment/Core Infra/Public API).
  - *Flow:* Boss writes full `SPEC.md` & `TASKS.md` (read-only) → STOP and request Critic (Argon) Red-Team → Isolated Workers execute → Deterministic QA → Independent Reviewer (Argon) approves `git diff`.

## 2. Non-Negotiable Invariants (All Tiers)
1. **Scope Lock:** When `.workflow/SPEC.md` exists, ONLY create/edit files listed in `File Whitelist`. NEVER touch `File Blacklist` or perform unsolicited "helpful" refactoring outside scope. If an unlisted file must change, STOP and ask the user.
2. **Anti-Cheating:** NEVER delete, comment out, `.skip()`, or weaken existing tests/assertions to force green builds. NEVER add `@ts-ignore`, `any`, `# noqa`, `eslint-disable`, or empty `try/catch` swallowing errors unless explicitly approved in `SPEC.md`.
3. **Dependency Freeze:** NEVER install/upgrade packages or modify `.env*` / lockfiles unless explicitly requested.
4. **Circuit Breaker (Quota Protection):** If lint, build, or test fails **2 consecutive times** on the same error group, STOP editing immediately. Extract max 30 relevant log lines + root-cause hypothesis into `.workflow/BLOCKER.md` and hand back to Boss.
5. **Definition of Done:** Never claim completion from reading code alone. Run the exact verification commands from `.workflow/PROJECT_PROFILE.md` or `SPEC.md` and report actual pass/fail output concisely.

## 3. Project Conventions (python-ai-platform)
- **Architecture:** Personal static app (NO auth, NO backend). Progress persists in `localStorage` via `apps/web/src/lib/storage.ts`. Content pipeline: `curriculum/` → `tools/build_content.py` → `apps/web/src/generated/` (gitignored). Client-side EN/VI via `next-intl` (update both `apps/web/messages/en.json` and `vi.json`; no hardcoded UI strings).
- **Dose Design System (`apps/web/design.md`):** No raw color literals (`#hex`/`oklch`) in `.tsx`, no `backdrop-blur`, no `transition-all`, tap targets ≥ 44px (`.hit`), fonts Be Vietnam Pro (400/500/700) + JetBrains Mono.
- **Bilingual Content Parity:** Every lesson/exercise/quiz/exam has EN + VI with identical IDs, structure, mermaid line counts, and code blocks (never translate code or `# output` comments). Vietnamese prose addresses the reader as `"bạn"` (never `"ta"`/`"chúng ta"` except `"người ta"`), keeping English technical terms with a Vietnamese gloss on first use.
- **Exercises & Tests:** `starter.py` must fail 100% (`EXERCISE_TARGET=starter`); `solution.py` + alternatives must pass 100% under BOTH `pytest` and `tools/pyrunner/runner.py` (supported pytest subset only). Solutions must not copy ≥5 consecutive lines verbatim from `lesson.*.md`.
- **Runtime & Tooling (Windows):** LLM calls use `pyai_llm` (zero network/API keys); time uses standard `FakeClock`; HF models use `local_files_only=True`; phase 4+ code runs clean under `python -W error` (Pyodide `int32` safe). Only `runner: local` lessons/exercises may import `torch`/`transformers`/`fastapi`/`uvicorn`. Run `uv run python -m pytest` (never `uv run pytest`) and `pnpm.cmd` in PowerShell; stop dev server before `web build`.
