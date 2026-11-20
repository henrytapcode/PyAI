---
name: workflow-commander
description: "Guide the 4-account Gemini Pro workflow (Antigravity App + AGY CLI), effort levels, phase transitions, quota failover, and ready-to-copy commands from .workflow/ state."
---
# Workflow Commander (4-Account Gemini Pro Operating Guide)

## 1. Account & Role Allocation
- **Acc 1 (Antigravity App — Gemini 4 Neon):** Boss, Spec Architect, large-codebase reading, Tier 1/2/3 triage, resolving `.workflow/BLOCKER.md`, updating `.workflow/SPEC.md` & `.workflow/TASKS.md`. For **Tier 1**, execute directly via `Orchestrator (Neon)` inside the App.
- **Acc 2 & Acc 3 (AGY CLI — Gemini 4 Hydrogen / 3.8 Flash):** Worker Pool & QA executing `/run-workflow` (parallel isolated branches for `[PARALLEL]`, sequential for `[SERIAL]`). Strictly obey `File Whitelist` and Circuit Breaker (2 consecutive failures on the same error group → write `.workflow/BLOCKER.md` and STOP). When Acc 2 hits `Individual quota reached`, switch to Acc 3 and re-run the exact same `/run-workflow` command to resume remaining `[ ]` tasks in `.workflow/TASKS.md`.
- **Acc 4 (AGY CLI — Gemini 4 Argon):**
  - **Phase 2 (Adversarial Critic — Tier 3 only):** Red-team `.workflow/SPEC.md` & `.workflow/TASKS.md` (read-only) → write `.workflow/CRITIQUE.md`.
  - **Phase 5 (Persistent Final Reviewer):** Audit `git diff` + verification logs (read-only) → write `.workflow/REVIEW.md`. Merge requires `VERDICT: APPROVE`.

## 2. Default Effort Matrix (ALWAYS include `--effort` in CLI commands)
| Model | Default `--effort` | Escalation / Adjustment Rule |
|---|---|---|
| **Gemini 4 Neon** | `high` | Use `xhigh` ONLY for critical `BLOCKER.md` or hardest architectural problems. |
| **Gemini 4 Argon** | `high` | Use `medium` for small, low-risk diffs. |
| **Gemini 4 Hydrogen** | `medium` | Use `high` for hard tasks. **NEVER** use `xhigh`. |
| **Gemini 3.8 Flash** | `low` / `medium` | Use for lightweight/repetitive tasks or quick QA checks. |
| **Gemini Flash-Lite** | `minimal` / `low` | Use only for trivial/mechanical chores. |

## 3. Navigation Protocol (Mandatory Response Format)
Whenever the user asks *"tiếp theo làm gì?"*, *"xong bước này rồi"*, *"gặp lỗi"*, or *"hết quota"*:
1. **Inspect live state first:** Read existing files in `.workflow/` (`PROJECT_PROFILE.md`, `SPEC.md`, `TASKS.md`, `CRITIQUE.md`, `BLOCKER.md`, `REVIEW.md`) and run `git status --short`.
2. **State routing logic:**
   - If `.workflow/BLOCKER.md` exists → Route to **Acc 1 (App — Neon `--effort xhigh`)** to resolve root cause and update `SPEC.md`/`TASKS.md`.
   - Else if Tier 3 and `.workflow/CRITIQUE.md` does not exist → Route to **Acc 4 (CLI — Argon `--effort high`)** for Phase 2 Adversarial Critic.
   - Else if `.workflow/CRITIQUE.md` has unresolved `[BLOCKER]` items → Route to **Acc 1 (App — Neon `--effort high`)** to patch `SPEC.md`/`TASKS.md`.
   - Else if `.workflow/TASKS.md` has unchecked `[ ]` tasks in active wave → Route to **Acc 2 (CLI — Hydrogen `--effort medium`, or `high` for hard tasks)** to run `/run-workflow` (on quota exhaustion → swap to **Acc 3** with identical command).
   - Else if all active `[ ]` tasks are `[x]` and `.workflow/REVIEW.md` lacks `VERDICT: APPROVE` → Route to **Acc 4 (CLI — Argon `--effort high`, or `medium` for small diff)** for Phase 5 Final Review.
   - Else if `.workflow/REVIEW.md` has `VERDICT: APPROVE` → Instruct user to merge/commit cleanly and start next wave or task.
3. **Respond concisely in Vietnamese using this exact 3-part template:**
   1. **Pha & trạng thái thực tế:** (cite exact `.workflow/*` state and `git status`).
   2. **Chuyển sang:** `[Acc mấy | App hay CLI | Model | --effort <level>]`.
   3. **Lệnh terminal (nếu có) + đúng 1 khối prompt sẵn sàng copy-paste.**

## 4. Reference CLI Command Shapes
- **Acc 4 — Phase 2 Critic (Tier 3):**
  ```bash
  agy --model argon --effort high
  ```
- **Acc 2 / Acc 3 — Phase 3–4 Worker Pool (`/run-workflow`):**
  ```bash
  agy --model hydrogen --effort medium
  # (Use --effort high for complex tasks; NEVER xhigh. On quota error, switch to Acc 3 and re-run.)
  ```
- **Acc 4 — Phase 5 Final Reviewer:**
  ```bash
  agy --model argon --effort high
  # (Use --effort medium for small diffs.)
  ```
- **Acc 1 — Boss / Blocker Escalation (App):**
  Switch to Antigravity App (Gemini 4 Neon, effort `high`; use `xhigh` only for severe `BLOCKER.md`).
