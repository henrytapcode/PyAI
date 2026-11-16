# Validation report for AskRequest

**What it shows:** Sending one valid payload and four different invalid payloads to `POST /ask` so you can compare the HTTP status codes and Pydantic error types.

**Step by step**
1. Lines 10–12 define `AskRequest` with `question` (`min_length=1`, `max_length=200`) and `top_k` (`default=3`, `ge=1`, `le=5`).
2. Lines 15–17 register `POST /ask`, which runs only after Pydantic validates the JSON body.
3. Lines 20–27 define five test payloads: one valid, one missing `question`, one empty string, one out-of-range integer (`top_k=9`), and one wrong type (`top_k="many"`).
4. Lines 29–37 send each payload through `TestClient` and print a compact report showing the status code and the first error's `(loc, type)`.

**Notice:** Each failure produces a specific machine-readable `type` (`missing`, `string_too_short`, `less_than_equal`, `int_parsing`), while `ask()` only ever sees clean, validated data on case 1.

**Try it yourself:** Add a payload with `"top_k": 0` and confirm it fails with `greater_than_equal` because `ge=1` forbids zero.
