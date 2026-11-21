from dataclasses import dataclass, field


@dataclass
class Chat:
    title: str
    messages: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.messages.append(message)

    def count(self) -> int:
        return len(self.messages)


@dataclass(frozen=True)
class GenerationConfig:
    model: str
    temperature: float = field(default=0.7)
    max_tokens: int = field(default=256)
