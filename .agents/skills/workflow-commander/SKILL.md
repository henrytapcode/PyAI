---
name: workflow-commander
description: "Guide the 4-account Gemini Pro workflow (100% Antigravity Desktop App), effort levels, phase transitions, quota failover, and ready-to-copy prompts from .workflow/ state."
---
# Workflow Commander (100% Antigravity App — 4-Account Quota Pool)

## 1. Account & Role Architecture (App-Only + Quota Rotation)
- **100% Antigravity Desktop App (NO CLI):** All phases run inside Antigravity Desktop App on `d:\Proj\python-ai-platform` (auto-loads `GEMINI.md`, zero `outside workspace` issues, unified iOS Remote Control via `https://antigravity.google`).
- **1 Active Account + Ring Rotation (`Acc 1 → Acc 2 → Acc 3 → Acc 4 → Acc 1`):**
  - Keep **ONE Active Account** signed in across all phases of a wave (**0 mid-wave logins**, **4× total Argon weekly + Neon + Hydrogen quotas** across the pool).
  - **Role isolation comes from opening a fresh `New Conversation` + switching Model + file-based state (`.workflow/*`), NEVER mixing roles in one conversation:**
    - **Boss / Spec Architect (Boss Conversation — Gemini 4 Neon):** Large-codebase reading, Tier 1/2/3 triage, authoring/patching `.workflow/SPEC.md` & `.workflow/TASKS.md`, resolving `.workflow/BLOCKER.md`. For **Tier 1**, execute directly in Boss conversation.
    - **Worker Pool & QA (New Conversation — Gemini 4 Hydrogen / 3.8 Flash):** Executes Wave tasks in order (`[SERIAL]` first, then parallel subagents `invoke_subagent` / `run_workflow` for disjoint `[PARALLEL]` tasks). Strictly obeys `File Whitelist` and Circuit Breaker (2 consecutive failures on the same error group → write `.workflow/BLOCKER.md` and STOP).
    - **Adversarial Critic & Final Reviewer (Fresh New Conversation — Gemini 4 Argon):**
      - **Phase 2 (Tier 3 only):** Red-team `.workflow/SPEC.md` & `.workflow/TASKS.md` (read-only) → write `.workflow/CRITIQUE.md`.
      - **Phase 5 (Final Review):** Audit `git diff` + verification logs (read-only) → write `.workflow/REVIEW.md`. Merge requires `VERDICT: APPROVE`.
  - **When to Rotate Account:** ONLY when the active account hits a quota/rate limit (5-hour cap or Argon weekly cap). Sign out → Sign in to next account in ring (`1 → 2 → 3 → 4 → 1`) in App Settings, open a **New Conversation** with the same Model & Effort, and send the 1-line `.workflow/NEXT_PROMPT.md` trigger to resume unchecked `[ ]` tasks in `.workflow/TASKS.md`.

## 2. Default Effort Matrix
| Model | Default Effort | Escalation / Token-Saving Rule |
|---|---|---|
| **Gemini 4 Neon** | `Medium` (routing/triage/small edits) / `High` (SPEC & complex bugs) | Moderate token discipline: read `.workflow/*` first, use grep/line-ranges on files >150 lines, batch reads, run targeted tests first. Use `xHigh` ONLY for severe `BLOCKER.md`. |
| **Gemini 4 Argon** | `Medium` (lean) / `High` (strict) | Argon has a separate weekly limit and burns tokens fast: default `Medium` + strict read/line caps in `NEXT_PROMPT.md`; reserve `High` for critical security/core-infra/large-diff audits. |
| **Gemini 4 Hydrogen** | `Medium` | Use `High` for hard tasks. **NEVER** use `xHigh`. Prefer parallel subagents over `/teamwork` when `SPEC.md` already locks disjoint files. |
| **Gemini 3.8 Flash** | `Low` / `Medium` | Use for lightweight/repetitive tasks or quick QA checks. |
| **Gemini Flash-Lite** | `Minimal` / `Low` | Use only for trivial/mechanical chores. |

## 3. Navigation Protocol (Zero-Copy `.workflow/NEXT_PROMPT.md`)
- **Mandatory End-of-Task Rule (Every Turn):** At the end of EVERY completed task or phase (even if the user did not explicitly ask *"việc tiếp theo"*), ALWAYS update `.workflow/NEXT_PROMPT.md` for the next phase and end your response with the 3-part Next Step block below.
- Whenever transitioning phases or handing off to Worker / Critic / Reviewer, ALWAYS write the complete, self-contained instructions directly into `.workflow/NEXT_PROMPT.md` (overwriting the previous prompt). The user opens a **New Conversation** in Antigravity App, selects the target Model & Effort, and sends the exact 1-line trigger:
  `Đọc và thực thi đúng toàn bộ chỉ thị trong .workflow/NEXT_PROMPT.md`

Whenever the user asks *"tiếp theo làm gì?"*, *"xong bước này rồi"*, *"gặp lỗi"*, or *"hết quota"*:
1. **Inspect live state first:** Read existing files in `.workflow/` (`PROJECT_PROFILE.md`, `SPEC.md`, `TASKS.md`, `CRITIQUE.md`, `BLOCKER.md`, `REVIEW.md`) and run `git status --short`.
2. **State routing logic (all on current Active Account; rotate Acc ONLY on quota limit):**
   - If `.workflow/BLOCKER.md` exists → Handle directly in **Boss Conversation (Neon `High`, escalate to `xHigh` only if severe)** to resolve root cause and update `SPEC.md`/`TASKS.md`.
   - Else if Tier 3 and `.workflow/CRITIQUE.md` does not exist → Route to **New Conversation (Gemini 4 Argon | Effort: `Medium`)** for Phase 2 Adversarial Critic.
   - Else if `.workflow/CRITIQUE.md` has unresolved `[BLOCKER]` items → Patch `SPEC.md`/`TASKS.md` in **Boss Conversation (Neon `Medium`/`High`)**.
   - Else if `.workflow/TASKS.md` has unchecked `[ ]` tasks in active wave → Route to **New Conversation (Gemini 4 Hydrogen | Effort: `Medium`)** for Phase 3–4 Worker execution (on quota exhaustion → rotate Acc in App Settings → open New Conversation and send the same 1-line trigger).
   - Else if all active `[ ]` tasks are `[x]` and `.workflow/REVIEW.md` lacks `VERDICT: APPROVE` → Route to **New Conversation (Gemini 4 Argon | Effort: `Medium`, or `High` for large/high-risk diffs)** for Phase 5 Final Review.
   - Else if `.workflow/REVIEW.md` has `VERDICT: APPROVE` → Instruct user to commit cleanly and start next wave or task.
3. **Write `.workflow/NEXT_PROMPT.md`** for any handoff to a New Conversation.
4. **Respond concisely in Vietnamese using this exact 3-part template:**
   1. **Pha & trạng thái thực tế:** (cite exact `.workflow/*` state and `git status`).
   2. **Thao tác trong Antigravity App:** `[Giữ nguyên Active Acc (chỉ đổi Acc nếu hết quota) | New Conversation hay tiếp ở Boss | Model | Effort: <level>]`.
   3. **Đúng 1 dòng prompt gọi `.workflow/NEXT_PROMPT.md`** (copy-paste ready).
