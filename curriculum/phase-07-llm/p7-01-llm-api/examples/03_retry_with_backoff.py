# Retry transient RateLimitError with exponential backoff without sleeping.
from pyai_llm import FakeLLM, RateLimitError


def call_with_retry(
    client: FakeLLM,
    messages: list[dict[str, str]],
    max_attempts: int = 3,
) -> str:
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.chat(messages)
            print(f"Attempt {attempt}: succeeded")
            return resp.content or ""
        except RateLimitError as err:
            wait = 0.5 * 2 ** (attempt - 1)
            print(f"Attempt {attempt}: {err} (would wait {wait}s)")
            if attempt == max_attempts:
                raise
    raise RuntimeError("unreachable")


msgs = [{"role": "user", "content": "What is RAG?"}]

print("--- Case 1: recovers after 2 failures ---")
reply = call_with_retry(FakeLLM(fail_times=2), msgs, max_attempts=3)
print("Reply:", reply)

print("--- Case 2: fails all 3 attempts ---")
try:
    call_with_retry(FakeLLM(fail_times=5), msgs, max_attempts=3)
except RateLimitError as err:
    print("Caught after retries exhausted:", err)
