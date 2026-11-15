# Stateful ChatSession class that resends history and tracks total tokens.
from dataclasses import dataclass, field

from pyai_llm import FakeLLM


@dataclass
class ChatSession:
    client: FakeLLM
    system: str
    history: list[dict[str, str]] = field(default_factory=list)
    total_tokens: int = 0

    def __post_init__(self) -> None:
        if not self.history:
            self.history.append({"role": "system", "content": self.system})

    def ask(self, text: str) -> str:
        self.history.append({"role": "user", "content": text})
        resp = self.client.chat(self.history)
        reply = resp.content or ""
        self.history.append({"role": "assistant", "content": reply})
        self.total_tokens += resp.usage.total_tokens
        return reply


session = ChatSession(client=FakeLLM(), system="You are a concise study tutor.")
for prompt in ["What is RAG?", "What is temperature?", "What is a token?"]:
    answer = session.ask(prompt)
    print(f"Q: {prompt}")
    print(f"A: {answer}")
    print(f"history length: {len(session.history)}")

print(f"final history length: {len(session.history)}")
print(f"total_tokens: {session.total_tokens}")
