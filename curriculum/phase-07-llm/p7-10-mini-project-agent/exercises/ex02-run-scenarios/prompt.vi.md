Viết hai hàm `run_scenario(scenario, toolbox, make_client)` và `summarize(results)` để chạy các kịch bản agent tất định kèm giới hạn an toàn và định dạng báo cáo đạt/trượt gọn gàng. Viết code bên trong hai hàm và `return` kết quả.

**Ví dụ**

```python
res = run_scenario(scenario, toolbox, lambda script: FakeLLM(script=script))
# res -> {
#     "name": "happy_lookup",
#     "passed": True,
#     "stopped_reason": "final",
#     "tools": ["lookup_order"],
#     "reasons": [],
# }
print(summarize([res]))
# ["passed: 1/1", "all passed"]
```

**Quy tắc**

- Trong `run_scenario(scenario: dict, toolbox, make_client) -> dict`:
  - Gọi `make_client(list(scenario["script"]))` đúng một lần để tạo client mới cho kịch bản mà không làm thay đổi `scenario`.
  - Đọc `max_steps = scenario.get("max_steps", 6)`, `token_budget = scenario.get("token_budget")` và `approve = scenario.get("approve")`.
  - Ở mỗi bước (`1 .. max_steps`), gọi `client.chat(messages, tools=toolbox.schemas())`, cộng dồn `resp.usage.total_tokens`, rồi kiểm tra điều kiện dừng theo đúng thứ tự sau:
    1. `budget`: nếu `token_budget is not None` và tổng token `> token_budget`, dừng với `"budget"`.
    2. `final`: nếu `not resp.tool_calls`, lưu `resp.content or ""` làm câu trả lời cuối và dừng với `"final"`.
    3. `repeat`: lấy `tc = resp.tool_calls[0]` và `args = dict(tc.arguments)`; nếu bước đã thực thi ngay trước đó có cùng `(tool, args)`, dừng với `"repeat"`.
    4. `needs_approval` / `rejected`: nếu `toolbox.is_side_effect(tc.name)` là `True`: khi `approve is None`, dừng ngay với `"needs_approval"`; ngược lại gọi `approve(tc.name, dict(args))`, nếu trả về `False` thì dừng ngay với `"rejected"`. Trong cả hai trường hợp bị chặn, tuyệt đối không gọi `toolbox.call(...)` và không thêm `tc.name` vào `tools`.
  - Ngược lại, gọi `obs = toolbox.call(tc.name, dict(args))`, nối message `assistant` (`content=None`, `tool_calls=[{"id": tc.id, "name": tc.name, "arguments": args}]`) và `tool` (`tool_call_id=tc.id`, `content=obs`), rồi ghi `tc.name` vào `tools`.
  - Nếu chạy hết `max_steps` mà chưa dừng, gán `stopped_reason = "max_steps"`.
  - Tạo `reasons: list[str]` theo đúng thứ tự cố định `["stopped_reason", "tools", "answer"]`:
    - thêm `"stopped_reason"` nếu `stopped_reason != expect["stopped_reason"]`;
    - thêm `"tools"` nếu `tools != expect["tools"]`;
    - thêm `"answer"` nếu `expect.get("answer_contains")` không rỗng và không xuất hiện (không phân biệt hoa/thường) trong `answer`.
  - Trả về `{"name": scenario["name"], "passed": len(reasons) == 0, "stopped_reason": stopped_reason, "tools": tools, "reasons": reasons}`.
- Trong `summarize(results: list[dict]) -> list[str]`:
  - Dòng đầu tiên là `f"passed: {passed_count}/{len(results)}"`.
  - Với mỗi kết quả có `not r["passed"]`, thêm dòng `f"FAIL {r['name']}: {', '.join(r['reasons'])}"` theo đúng thứ tự đầu vào.
  - Nếu không có kịch bản nào trượt, thêm `"all passed"` ở cuối danh sách.
