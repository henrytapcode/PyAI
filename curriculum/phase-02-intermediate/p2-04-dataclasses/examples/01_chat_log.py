# A chat log made of Message dataclasses, ready to send to an API as a list of dicts.
import json
from dataclasses import asdict, dataclass, field


@dataclass
class Message:
    role: str
    content: str
    tags: list = field(default_factory=list)

    def word_count(self):
        return len(self.content.split())


log = [
    Message("system", "You are a helpful tutor."),
    Message("user", "What is a dataclass?", tags=["question"]),
    Message("assistant", "A class that writes the boring code for you."),
]

total_words = 0
for message in log:
    total_words += message.word_count()
    print(message)

print("total words:", total_words)
print(log[0] == Message("system", "You are a helpful tutor."))

payload = []
for message in log:
    payload.append(asdict(message))
print(json.dumps(payload[1]))
