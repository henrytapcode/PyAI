Viết hàm `run_with_tools(client, question, tools, registry, max_rounds=3)` trong `starter.py` để chạy vòng lặp gọi tool có giới hạn bước và điều phối an toàn.

Viết code bên trong hàm và `return` bộ đôi `(final_answer, called)`.

## Ví dụ

```python
run_with_tools(FakeLLM(), "What is the weather in Hanoi?", [weather_tool], {"get_weather": get_weather})
# -> ("Based on the tool result: 31C and sunny", ["get_weather"])

run_with_tools(FakeLLM(), "Tell me a joke", [weather_tool], {"get_weather": get_weather})
# -> ("(fake model) I received: Tell me a joke", [])
```

## Quy tắc

- Khởi tạo `messages = [{"role": "user", "content": question}]` và lặp tối đa `max_rounds` vòng:
  - Gọi `client.chat(messages, tools=tools)`.
  - Nếu `resp.tool_calls` rỗng, trả về `(resp.content or "", called)`.
  - Ngược lại, nối `{"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": dict(tc.arguments)} for tc in resp.tool_calls]}`.
  - Với từng `tc` trong `resp.tool_calls`:
    - Nếu `tc.name` không có trong `registry`, dùng chuỗi `f"error: unknown tool {tc.name}"`.
    - Ngược lại, thêm `tc.name` vào `called`, loại bỏ giá trị `""` / `None` của các tham số tùy chọn (không nằm trong danh sách `"required"` của tool đó), rồi gọi `registry[tc.name](**clean_args)` trong `try/except Exception` (bắt ngoại lệ thành `f"error: {err}"`).
    - Nếu kết quả hàm là `dict`, chuyển thành chuỗi bằng `json.dumps(out)`; kiểu khác chuỗi dùng `str(out)`.
    - Nối `{"role": "tool", "tool_call_id": tc.id, "content": result}` ngay sau message `assistant`.
- Nếu hết `max_rounds` vòng mà vẫn chưa có câu trả lời cuối, trả về `("stopped: too many tool calls", called)`.
- Không làm thay đổi danh sách `tools` hay dictionary `registry`.
