---
name: workflow-commander
description: "Guide the 4-account Gemini Pro workflow (Single-Conversation Orchestrator via swarm in Antigravity Desktop App), effort levels, phase transitions, quota failover, and fallback prompts from .workflow/ state."
---
# Workflow Commander (Single-Conversation Orchestrator — Antigravity Desktop App)

## 1. Architecture (1 Boss Conversation + Native `swarm` Isolation)
- **100% Antigravity Desktop App (NO CLI):** Stay in **ONE Boss Conversation** (`Orchestrator (Neon)` or `Gemini 4 Neon`, Effort `Medium`/`High`) on `d:\Proj\python-ai-platform`. No copy-pasting prompts across tabs!
- **Role isolation & parallel execution via `swarm` (NOT manual tab switching):**
  - **Tier 1 (1–2 files):** Execute directly in Boss conversation (zero swarm overhead).
  - **Tier 2 / Tier 3:** Boss writes `.workflow/SPEC.md` & `.workflow/TASKS.md`, then dispatches fresh isolated `swarm` workers (each starts with an empty conversation — zero Boss bias) with `workspace: "inherit"` whenever tasks own disjoint files (avoids Windows git worktree/merge overhead):
    - **Phase 2 Critic (Tier 3):** `swarm(add, name="critic", model="gemini-4-argon-medium", workspace="inherit")` → writes `.workflow/CRITIQUE.md` (read-only on source).
    - **Phase 3–4 Workers (`[PARALLEL]` disjoint tasks):** `swarm(add, ..., model="gemini-4-hydrogen-medium", workspace="inherit")` → each worker runs its own targeted tests/linters before reporting done. Boss runs `[SERIAL]` integration & full QA gates (or delegates to a single QA worker).
    - **Phase 5 Final Reviewer:** `swarm(add, name="reviewer", model="gemini-4-argon-medium", workspace="inherit")` (or `high` for large/high-risk diffs) → audits `git diff` → writes `.workflow/REVIEW.md`. Merge requires `VERDICT: APPROVE`.
  - **Clean up workers:** `swarm(kill)` finished workers after their wave/phase lands so the roster stays clean.
- **In-Account Multi-Pool Failover (`swarm(model)`):** Check `swarm(models, all=true)` before spawning. If a worker hits its 5h Gemini quota, switch it in-place with `swarm(model)` to an available pool (e.g., `claude-sonnet-5-5-medium`) without losing conversation state.
- **Account Rotation Fallback (`Acc 1 → 2 → 3 → 4 → 1`):** ONLY when ALL usable model pools on the Active Account are exhausted, write `.workflow/NEXT_PROMPT.md`, ask the user to rotate account in App Settings, open a **New Conversation** (`Orchestrator (Neon)` / `Gemini 4 Neon`), and send:
  `Đọc và thực thi đúng toàn bộ chỉ thị trong .workflow/NEXT_PROMPT.md`

## 2. Default Model & Effort Matrix
| Role | Recommended Model | Escalation / Token-Saving Rule |
|---|---|---|
| **Boss / Orchestrator** | `Orchestrator (Neon)` or `Gemini 4 Neon` (`Medium` / `High`) | **NEVER** use `Orchestrator (Argon)` as Boss (burns Argon's weekly cap). Use `xHigh` ONLY for severe `BLOCKER.md`. |
| **Critic & Reviewer** | `gemini-4-argon-medium` | Argon has a separate weekly cap: default `medium` + strict turn/read/line caps; reserve `high` for critical security/core-infra/large-diff audits. |
| **Execution Workers** | `gemini-4-hydrogen-medium` | Fallback to `claude-sonnet-5-5-medium` via `swarm(model)` if 5h Gemini pool runs low. **NEVER** use `xHigh`. |
| **Lightweight Chores** | `gemini-3.8-flash-medium` | Use for simple single-file edits or quick mechanical checks. |

## 3. State & Compaction Protocol
- **Disk State Is Source of Truth:** Always persist `.workflow/{SPEC,TASKS,CRITIQUE,REVIEW,BLOCKER}.md` on disk so work survives crashes, compaction, or Account rotation.
- **Boss Conversation Compaction Rule:** Because the Boss conversation persists across waves, append a 1-line `/compact` reminder at clean checkpoints (after committing a wave, starting a new milestone, or after ≥ 8–10 heavy turns/logs) once `.workflow/*` is saved on disk.
- **When User Triggers (`"tiếp theo làm gì?"`, `"xong bước này rồi"`, `"gặp lỗi"`, `"hết quota"`):**
  1. Inspect `.workflow/*` and `git status --short`.
  2. Auto-advance via `swarm` in the current Boss conversation whenever quota permits (do not ask the user to manually copy-paste unless Account rotation is required).
  3. Only when rotating accounts or stopping at a user approval gate, write `.workflow/NEXT_PROMPT.md` and present the concise 3-part Vietnamese summary: (1) Pha & trạng thái thực tế, (2) Thao tác trong Antigravity App, (3) 1 dòng prompt gọi `.workflow/NEXT_PROMPT.md`.
