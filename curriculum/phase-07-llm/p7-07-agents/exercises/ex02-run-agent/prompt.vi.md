Viết hàm `run_agent(client, task, tools, registry, max_steps=5, token_budget=None)` trong `starter.py` để chạy vòng lặp agent nhiều bước có ghi trace và kiểm tra các điều kiện dừng.

Viết code bên trong hàm và `return` một dictionary kết quả.

## Ví dụ

```python
run_agent(FakeLLM(script=script), "When will order 1042 arrive?", tools, registry)
# -> {
#     "answer": "Order 1042 arrives in 2 business days.",
#     "stopped_reason": "final",
#     "steps": 3,
#     "trace": [
#         {"step": 1, "tool": "lookup_order", "args": {"order_id": "1042"}, "observation": "shipped"},
#         {"step": 2, "tool": "estimate_delivery", "args": {"carrier": "FastPost"}, "observation": "2 business days"},
#     ],
# }
```

## Quy tắc

- Trả về dict với đúng các key: `"answer"` (`str`, chuỗi rỗng `""` nếu dừng sớm), `"stopped_reason"` (`"final"`, `"max_steps"`, `"repeat"` hoặc `"budget"`), `"steps"` (`int`, số lần gọi `client.chat`) và `"trace"` (list các dict `{"step", "tool", "args", "observation"}`).
- Khởi tạo `messages = [{"role": "user", "content": task}]` và lặp `step` từ `1` đến `max_steps`:
  - Gọi `resp = client.chat(messages, tools=tools)` rồi cộng `resp.usage.total_tokens` vào tổng token.
  - Kiểm tra điều kiện dừng theo đúng thứ tự:
    1. **budget**: nếu `token_budget is not None` và `total_tokens > token_budget`, trả về ngay với `stopped_reason="budget"`.
    2. **final**: nếu `not resp.tool_calls`, trả về ngay với `answer=resp.content or ""` và `stopped_reason="final"`.
    3. **repeat**: kiểm tra tool call đầu tiên `tc = resp.tool_calls[0]` (`args = dict(tc.arguments)`). Nếu `trace` không rỗng và mục ngay trước có cùng `tool` và `args`, trả về ngay với `stopped_reason="repeat"` mà không chạy tool.
  - Ngược lại, điều phối `tc` an toàn:
    - Nếu `tc.name` không có trong `registry`, quan sát là `f"error: unknown tool {tc.name}"`.
    - Nếu có, lọc bỏ giá trị `""` / `None` khỏi các tham số tùy chọn (không nằm trong danh sách `"required"` của tool đó) rồi gọi `registry[tc.name](**clean_args)` trong `try/except Exception` (bắt ngoại lệ thành `f"error: {err}"`).
    - Nếu kết quả là `dict`, đổi sang chuỗi bằng `json.dumps(out)`, còn lại dùng `str(out)`.
  - Nối `{"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}]}` và `{"role": "tool", "tool_call_id": tc.id, "content": observation}` vào `messages`.
  - Nối `{"step": step, "tool": tc.name, "args": args, "observation": observation}` vào `trace`.
- Nếu hết `max_steps` mà chưa trả về, trả về `stopped_reason="max_steps"` và `steps=max_steps`.
- Không làm thay đổi `tools` hoặc `registry`.
