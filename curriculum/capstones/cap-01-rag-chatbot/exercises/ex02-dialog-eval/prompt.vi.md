Hãy cài đặt bộ đánh giá hội thoại chuẩn và cổng hồi quy (`score_turn`, `run_dialog_eval`, và `compare_to_baseline`) trong `starter.py`. Khác với đoạn code rút gọn ở §5, bài làm của bạn phải khởi tạo bot tách biệt qua `make_bot()` cho từng dialog, trả về lý do lỗi theo đúng thứ tự ưu tiên, đối chiếu baseline theo khóa `(dialog, turn)`, tách riêng các lượt `new`, gom danh sách `failures`, và áp đặt ngưỡng cổng `gate_ok`. Hãy viết code bên trong các hàm và `return` kết quả.

**Ví dụ**

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

**Quy tắc**

- Giữ nguyên hằng `REFUSAL = "I don't know based on the provided context."` và đúng chữ ký các hàm:
  - `score_turn(result: dict, turn: dict) -> str | None`
  - `run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]`
  - `compare_to_baseline(current: list[dict], baseline: list[dict], min_pass_rate: float = 0.8) -> dict`
- Mỗi dialog có dạng `{"id": str, "turns": [{"question": str, "expected_source": str | None, "expected_facts": list[str]}, ...]}`. Mỗi bot trả về từ `make_bot()` có phương thức `ask(question) -> {"answer": str, "sources": list[str], "rewritten": str}`.
- **`score_turn(result, turn)`**: trả về `None` nếu lượt đạt; ngược lại trả về **lý do đầu tiên** theo đúng thứ tự sau:
  - Khi `turn["expected_source"] is None`: đạt chỉ khi `result["answer"] == REFUSAL` và `result["sources"] == []`; ngược lại trả `"no_refusal"`.
  - Ngược lại: nếu `result["answer"] == REFUSAL` trả `"refused"`; nếu không thì nếu `turn["expected_source"] not in result["sources"]` trả `"wrong_source"`; nếu không thì nếu có bất kỳ fact nào trong `turn["expected_facts"]` không nằm trong `result["answer"]` (so không phân biệt hoa thường) trả `"missing_fact"`; đạt hết trả `None`.
- **`run_dialog_eval(make_bot, dialogs)`**: gọi `make_bot()` **một lần cho mỗi dialog** (bot mới để không lẫn lịch sử giữa các dialog), hỏi lần lượt các lượt trong dialog đó, và trả về danh sách theo đúng thứ tự dialog rồi lượt gồm các dict `{"dialog": dialog_id, "turn": n, "ok": bool, "reason": str | None}` với `n` đếm từ `1`.
- **`compare_to_baseline(current, baseline, min_pass_rate=0.8)`**:
  - Raise `ValueError` nếu `current` rỗng.
  - Ghép cặp theo khóa `(dialog, turn)`.
  - Tính `pass_rate = round(số_lượt_ok / len(current), 3)`.
  - `fixed`: danh sách tuple `(dialog, turn)` trước fail trong `baseline` nay ok trong `current`, theo thứ tự trong `current`.
  - `broken`: danh sách tuple `(dialog, turn)` trước ok trong `baseline` nay fail trong `current`, theo thứ tự trong `current`.
  - `new`: danh sách tuple `(dialog, turn)` có trong `current` nhưng không có trong `baseline`, theo thứ tự trong `current` (không tính vào `fixed` hay `broken`).
  - `failures`: danh sách tuple `(dialog, turn, reason)` của mọi lượt fail trong `current`, theo thứ tự trong `current`.
  - `gate_ok`: `not broken and pass_rate >= min_pass_rate`.
  - Trả về `{"pass_rate": pass_rate, "fixed": fixed, "broken": broken, "new": new, "failures": failures, "gate_ok": gate_ok}`.
