# Human-in-the-loop approval gate

**What it shows:** Pausing an agent with `stopped_reason == "needs_approval"` when it proposes a side-effect tool (`issue_refund`), then executing only after an explicit boolean approval.

**Step by step**
1. Lines 6–34 mark `"issue_refund"` in `APPROVAL_REQUIRED` while keeping `"lookup_order"` as a safe read-only tool.
2. Lines 37–58 run `run_with_approval()`: `lookup_order` runs automatically on step 1 and enters `trace`, while `issue_refund` on step 2 triggers an immediate pause returning `"needs_approval"` and `pending`.
3. Lines 61–64 define `handle_approval()`, which executes `REGISTRY[pending["tool"]]` only when `approved` is `True`.
4. Lines 67–81 run the scripted task and log the output for both `approved_by_human = False` and `approved_by_human = True`.

**Notice:** The agent never runs `issue_refund` inside the loop—it only proposes the pending action so application code outside the loop can enforce human sign-off.

**Try it yourself:** Add `"lookup_order"` to `APPROVAL_REQUIRED` and see how the agent pauses immediately on step 1 with an empty `trace`.
