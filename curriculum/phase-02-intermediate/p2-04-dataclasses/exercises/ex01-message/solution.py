from dataclasses import asdict, dataclass, field


@dataclass
class Message:
    """A chat message.

    Example:
        msg = Message("user", "Hi there")
        print(msg)                # Message(role='user', content='Hi there', tags=[])
        msg.word_count()          # 2
        msg.to_dict()             # {'role': 'user', 'content': 'Hi there', 'tags': []}
    """

    role: str
    content: str
    tags: list = field(default_factory=list)

    def word_count(self):
        return len(self.content.split())

    def to_dict(self):
        return asdict(self)
