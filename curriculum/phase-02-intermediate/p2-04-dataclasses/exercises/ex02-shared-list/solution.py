from dataclasses import dataclass, field


@dataclass
class Chat:
    title: str
    messages: list = field(default_factory=list)

    def add(self, text):
        self.messages.append(text)

    def count(self):
        return len(self.messages)


@dataclass(frozen=True)
class GenerationConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 256
