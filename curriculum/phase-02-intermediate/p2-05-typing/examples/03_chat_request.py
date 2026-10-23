# A typed request object for a chat API, with an optional system prompt.
from dataclasses import dataclass


@dataclass
class ChatRequest:
    model: str
    question: str
    system: str | None = None
    temperature: float = 0.0


def to_messages(request: ChatRequest) -> list[dict[str, str]]:
    messages = []
    if request.system is not None:
        messages.append({"role": "system", "content": request.system})
    messages.append({"role": "user", "content": request.question})
    return messages


plain = ChatRequest("demo-model", "Hello")
careful = ChatRequest("demo-model", "Hello", "Answer in one line.", 0.2)
print(plain)
print(to_messages(plain))
print(to_messages(careful))
