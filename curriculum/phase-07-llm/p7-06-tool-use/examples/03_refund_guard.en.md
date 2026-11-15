# Guarding side-effect tools

**What it shows:** Protecting a money-moving `issue_refund` tool with an allowlist, explicit human confirmation, and a `100.0` automatic cap while logging every decision.

**Step by step**
1. Lines 6–18 define `ORDERS`, `ALLOWED_TOOLS`, `MAX_AUTO_REFUND = 100.0`, an `ACTION_LOG` list, and `issue_refund()`.
2. Lines 21–34 implement `guarded_dispatch()`, which blocks any tool outside `ALLOWED_TOOLS`, blocks unconfirmed actions, and blocks amounts above `MAX_AUTO_REFUND` before `issue_refund()` ever runs.
3. Lines 37–42 configure a scripted `FakeLLM` proposing a `$45` refund (approved) and a `$250` refund (blocked).
4. Lines 49–65 run both requests through `guarded_dispatch()`, feed the tool outputs back into `scripted.chat()`, and print the full `ACTION_LOG`.

**Notice:** Even though the model proposed `amount=250.0` while application state had `user_confirmed=True`, the Python guard in `guarded_dispatch()` stopped the refund before `issue_refund()` ran and recorded the block in `ACTION_LOG`.

**Try it yourself:** Change `user_confirmed` to `False` on line 45 and observe that `ACTION_LOG` records `blocked: user confirmation required` even for the `$45` refund (while the scripted final reply stays fixed because this example uses a fixed reply script).
