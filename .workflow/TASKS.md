# TASKS: M5 Wave 2B — Resolve All 33 Pre-Existing Phase 1–8 Overlap Warnings

## Completed & Committed Checkpoints
- [x] M5 Wave 0 (`29fffe3`..`dcb33c8`): Capstone schema/tools/web support + `cap-01-rag-chatbot`.
- [x] M5 Wave 1 (`85c22f1`, Reviewer `VERDICT: APPROVE`): Web build unblock, `cap-02-tool-agent`, `mock-ai-engineer`, `mock-final`.
- [x] M5 Wave 2A (`75c032e`): Zero-dependency `tools/export_pdf.py` + `tools/test_export_pdf.py` (10/10 pass), `.gitignore` (`exports/`), updated `README.md`, `tasks/M5-PLAN.md`, `docs/*`.
- [x] M5 Wave 2B (`cbc1eee`, Reviewer `VERDICT: APPROVE` — 0 blocker, 0 minor): Refactored 26 Phase 1–8 `solution.py` files, resolved all 33 overlap warnings (`validate.py --fast` → `OK: 0 error(s), 0 warning(s)`), marked Milestone M5 100% complete.

---

## Wave 2B: Active Scope (TIER 3 — Locked to `.workflow/SPEC.md` — Request Lean Critic Red-Team Before Execution)

- [x] T1 [PARALLEL] (Batch A — Phases 1–3, 10 `solution.py` files, 14 warnings): Refactor `p1-06/{ex01,ex02}`, `p2-03/{ex01,ex02}`, `p2-04/ex02`, `p2-05/ex01`, `p2-09/{ex01,ex02}`, `p3-05/{ex01,ex02}` `solution.py` cleanly without touching any test/starter/lesson file. Done when `check_solution_overlap` reports 0 warnings on Phases 1–3, `uv run python -m pytest` + `validate.py --path` pass 100% on all 6 touched lessons, and `ruff check` is clean.
- [x] T2 [PARALLEL] (Batch B — Phases 4–6, 6 `solution.py` files, 7 warnings): Refactor `p4-06/ex02`, `p5-01/ex02`, `p5-05/ex02`, `p6-01/ex02`, `p6-03/ex02`, `p6-04/ex02` `solution.py` cleanly (preserving `python -W error`, `torch.manual_seed(0)`, `local_files_only=True`, cached HF `REPO`/`REV`). Done when `check_solution_overlap` reports 0 warnings on Phases 4–6, `uv run python -m pytest` + `validate.py --path` pass 100% on all 6 touched lessons, and `ruff check` is clean.
- [x] T3 [PARALLEL] (Batch C — Phases 7–8, 10 `solution.py` files, 12 warnings): Refactor `p7-02/{ex01,ex02}`, `p7-04/ex02`, `p7-05/ex02`, `p7-07/ex02`, `p7-08/ex01`, `p7-09/ex01`, `p8-01/{ex01,ex02}`, `p8-02/ex01` `solution.py` cleanly (preserving `pyai_llm`, FastAPI routes/schemas, and byte-identical `DOCKERFILE` in `p8-02/ex01`). Done when `check_solution_overlap` reports 0 warnings on Phases 7–8, `uv run python -m pytest` + `validate.py --path` pass 100% on all 8 touched lessons, and `ruff check` is clean.
- [x] T4 [SERIAL] (Files: `tasks/M5-PLAN.md`): Record Wave 2A commit `75c032e` and mark `7a–7c` (`m5-overlap-*`) complete so M5 table reflects 100% completion.
- [x] T5 [SERIAL] (Files: read-only verification across repo): Run full verification suite (`check_solution_overlap` == `TOTAL: 0`, `uv run ruff check curriculum`, `uv run python -m pytest curriculum -q`, `uv run python -m pytest tools packages -q`, `uv run python tools/validate.py --fast` == **`OK: 0 error(s), 0 warning(s)`**, `pnpm.cmd --filter web typecheck`) — ready for Phase 5 Independent Reviewer (Argon) audit before final M5 commit.
