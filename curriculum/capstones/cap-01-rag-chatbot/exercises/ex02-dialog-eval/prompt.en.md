Implement the golden dialog evaluator and regression gate (`score_turn`, `run_dialog_eval`, and `compare_to_baseline`) in `starter.py`. Unlike the simplified snippet in §5, your implementation must instantiate an isolated bot via `make_bot()` for each dialog, return prioritized per-turn failure reasons, key baseline comparisons by `(dialog, turn)`, track `new` turns separately, collect a `failures` list, and enforce the `gate_ok` threshold. Write your code inside the functions and `return` the results.

**Example**

```python
class StubBot:
    def __init__(self) -> None:
        self.replies = {
            "How long are pickup orders held?": {"answer": "Held for 7 days. [1]", "sources": ["pickup.md"], "rewritten": "How long are pickup orders held?"},
            "And photo ID?": {"answer": "Bring a photo ID. [1]", "sources": ["shipping.md"], "rewritten": "And photo ID?"},
            "Do you take crypto?": {"answer": REFUSAL, "sources": [], "rewritten": "Do you take crypto?"},
        }

    def ask(self, question: str) -> dict:
        return self.replies[question]


make_bot = StubBot

dialogs = [
    {
        "id": "d1",
        "turns": [
            {"question": "How long are pickup orders held?", "expected_source": "pickup.md", "expected_facts": ["7 days"]},
            {"question": "And photo ID?", "expected_source": "pickup.md", "expected_facts": ["photo ID"]},
        ],
    },
    {
        "id": "d2",
        "turns": [
            {"question": "Do you take crypto?", "expected_source": None, "expected_facts": []},
        ],
    },
]

current = run_dialog_eval(make_bot, dialogs)
# -> [
#     {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
#     {"dialog": "d1", "turn": 2, "ok": False, "reason": "wrong_source"},
#     {"dialog": "d2", "turn": 1, "ok": True, "reason": None},
# ]

baseline = [
    {"dialog": "d1", "turn": 1, "ok": True, "reason": None},
    {"dialog": "d1", "turn": 2, "ok": True, "reason": None},
]

compare_to_baseline(current, baseline, min_pass_rate=0.8)
# -> {
#     "pass_rate": 0.667,
#     "fixed": [],
#     "broken": [("d1", 2)],
#     "new": [("d2", 1)],
#     "failures": [("d1", 2, "wrong_source")],
#     "gate_ok": False,
# }
```

**Rules**

- Keep the constant `REFUSAL = "I don't know based on the provided context."` and match these exact signatures:
  - `score_turn(result: dict, turn: dict) -> str | None`
  - `run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]`
  - `compare_to_baseline(current: list[dict], baseline: list[dict], min_pass_rate: float = 0.8) -> dict`
- Each dialog is `{"id": str, "turns": [{"question": str, "expected_source": str | None, "expected_facts": list[str]}, ...]}`. Each bot returned by `make_bot()` exposes `ask(question) -> {"answer": str, "sources": list[str], "rewritten": str}`.
- **`score_turn(result, turn)`**: returns `None` if the turn passes; otherwise returns the **first** applicable failure reason in this exact order:
  - When `turn["expected_source"] is None`: passes only if `result["answer"] == REFUSAL` and `result["sources"] == []`; otherwise returns `"no_refusal"`.
  - Otherwise: if `result["answer"] == REFUSAL`, return `"refused"`; else if `turn["expected_source"] not in result["sources"]`, return `"wrong_source"`; else if any fact in `turn["expected_facts"]` is missing from `result["answer"]` (case-insensitive substring check), return `"missing_fact"`; else return `None`.
- **`run_dialog_eval(make_bot, dialogs)`**: call `make_bot()` **once per dialog** (fresh bot so conversation history never leaks across dialogs), ask that dialog's turns in order, and return a list ordered by dialog then turn of `{"dialog": dialog_id, "turn": n, "ok": bool, "reason": str | None}` where `n` starts at `1`.
- **`compare_to_baseline(current, baseline, min_pass_rate=0.8)`**:
  - Raise `ValueError` if `current` is empty.
  - Match turns by key `(dialog, turn)`.
  - Compute `pass_rate = round(passed_count / len(current), 3)`.
  - `fixed`: `(dialog, turn)` keys that failed in `baseline` and passed in `current`, in `current` order.
  - `broken`: `(dialog, turn)` keys that passed in `baseline` and failed in `current`, in `current` order.
  - `new`: `(dialog, turn)` keys present in `current` but absent from `baseline`, in `current` order (never counted in `fixed` or `broken`).
  - `failures`: list of `(dialog, turn, reason)` tuples for every failing entry in `current`, in `current` order.
  - `gate_ok`: `not broken and pass_rate >= min_pass_rate`.
  - Return `{"pass_rate": pass_rate, "fixed": fixed, "broken": broken, "new": new, "failures": failures, "gate_ok": gate_ok}`.
