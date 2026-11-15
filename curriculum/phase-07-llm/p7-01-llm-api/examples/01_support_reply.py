# Multi-turn support replies with token counts and hypothetical cost.
from pyai_llm import FakeLLM

PRICE_IN_PER_M = 0.50
PRICE_OUT_PER_M = 1.50

client = FakeLLM()
history: list[dict[str, str]] = [
    {"role": "system", "content": "You are a polite, concise support assistant."},
]
questions = [
    "What is RAG?",
    "What is a token?",
    "How do I reset my password?",
]

total_in = 0
total_out = 0

for turn, question in enumerate(questions, start=1):
    history.append({"role": "user", "content": question})
    resp = client.chat(history)
    history.append({"role": "assistant", "content": resp.content or ""})

    total_in += resp.usage.prompt_tokens
    total_out += resp.usage.completion_tokens

    print(f"Turn {turn}: {question}")
    print(f"Reply:  {resp.content}")
    print(
        f"Tokens: prompt={resp.usage.prompt_tokens}, "
        f"completion={resp.usage.completion_tokens}, "
        f"total={resp.usage.total_tokens}"
    )

cost = round((total_in / 1_000_000) * PRICE_IN_PER_M + (total_out / 1_000_000) * PRICE_OUT_PER_M, 6)
print(f"Grand total tokens: {total_in + total_out} (in={total_in}, out={total_out})")
print(f"Estimated cost (example pricing): ${cost:.6f}")
