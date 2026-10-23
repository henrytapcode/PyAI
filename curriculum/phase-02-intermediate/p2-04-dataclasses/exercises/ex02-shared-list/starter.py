from dataclasses import dataclass, field


# This file has 3 bugs. Run it, read the error, and fix them one at a time.
@dataclass
class Chat:
    title: str
    messages: list = []

    def add(self, text):
        self.messages.append(text)

    def count(self):
        return len(self.messages)


@dataclass
class GenerationConfig:
    model: str
    temperature = 0.7
    max_tokens: int = 256
