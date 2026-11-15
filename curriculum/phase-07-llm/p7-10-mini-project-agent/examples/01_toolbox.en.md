# Safe order-support toolbox

**What it shows:** Wrapping four shop tools behind a single `invoke()` dispatcher that enforces an allowlist, validates required arguments, drops extra parameters, catches runtime exceptions, and serializes dictionaries with `json.dumps()`.

**Step by step**
1. Lines 4–29 define the toy shop state (`ORDERS`, `SHIPMENTS`, `REFUNDS`) and the four Python tool functions.
2. Lines 32–52 register each function in `REGISTRY` alongside its JSON schema and `side_effect` flag.
3. Lines 55–69 implement `invoke(name, args)` to check the allowlist, validate `required`, filter to `properties`, and return `"error: ..."` strings instead of crashing.
4. Lines 72–80 run five success and failure test cases and print each resulting observation string.

**Notice:** Passing an unexpected `"extra": 1` field to `lookup_order` succeeds cleanly because `invoke()` filters `args` to the schema's `properties` before unpacking `**clean`.

**Try it yourself:** Add a sixth tuple `("missing_amt", "issue_refund", {"order_id": "1042"})` to `cases` and verify `invoke()` returns `"error: missing amount"` without writing to `REFUNDS`.
