from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str
    tags: list = field(default_factory=list)

    def word_count(self):
        count = 0
        for _word in self.content.split():
            count += 1
        return count

    def to_dict(self):
        return {"role": self.role, "content": self.content, "tags": self.tags}
