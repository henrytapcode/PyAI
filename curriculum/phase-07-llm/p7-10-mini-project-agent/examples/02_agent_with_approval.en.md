# Bounded agent with an approval gate

**What it shows:** Running `run_support_agent()` across three tasks—a read-only inquiry, an approved refund, and an over-policy refund blocked by `policy_gate`—while recording both `trace` and an `audit` log.

**Step by step**
1. Lines 5–35 define the orders, three tools (`issue_refund` marked with `True` for side effect), and schemas.
2. Lines 38–60 implement `run_support_agent()` with `max_steps`, `repeat` detection, and a side-effect check that calls `approve(name, args)` before running the function.
3. Lines 63–65 define `policy_gate()` to allow refunds only when `days_late >= 3` and `amount <= 20%` of the order total.
4. Lines 68–97 run all three scripted tasks and print `stopped_reason`, `pending`, step traces, `audit`, and `REFUNDS`.

**Notice:** On the rejected `$50` refund for order `1044`, `run_support_agent()` stops with `needs_approval`, populates `pending`, logs `ok=False by=policy_gate`, and leaves `REFUNDS` containing only order `1042`.

**Try it yourself:** Change the `"rejected "` script's refund amount from `50.0` to `24.0` (exact 20% of `$120.0`) and append a final reply string so the policy gate approves it cleanly.
