Hãy cài đặt hai hàm hỗ trợ gọi LLM đáng tin cậy và ước tính chi phí request:

1. `ask_with_retry(client, messages, max_attempts=3) -> tuple[str, int]`: gọi `client.chat(messages)` tối đa `max_attempts` lần. Khi thành công, trả về `(content, số_lần_đã_thử)`. Chỉ bắt và retry `RateLimitError`; nếu hết `max_attempts` vẫn lỗi thì ném lại đúng `RateLimitError` đó. Không retry các lỗi khác (như `ValueError`).
2. `estimate_cost(usage, price_in_per_m, price_out_per_m) -> float`: tính chi phí USD từ `usage.prompt_tokens` và `usage.completion_tokens` theo đơn giá cho mỗi 1 triệu token, làm tròn đến 6 chữ số thập phân.

Hãy viết code bên trong từng hàm và `return` kết quả.

**Ví dụ**

```python
client = FakeLLM(fail_times=2)
content, attempts = ask_with_retry(client, [{"role": "user", "content": "What is RAG?"}], max_attempts=3)
# attempts == 3

cost = estimate_cost(Usage(prompt_tokens=1000, completion_tokens=500, total_tokens=1500), 0.50, 1.50)
# 0.00125
```

**Quy tắc**

- Chỉ bắt và retry `RateLimitError`; các lỗi như `ValueError` phải dừng ngay ở lần thử đầu tiên.
- Không gọi `time.sleep()`.
- `estimate_cost` phải trả về `float` chuẩn của Python được làm tròn 6 chữ số thập phân.
