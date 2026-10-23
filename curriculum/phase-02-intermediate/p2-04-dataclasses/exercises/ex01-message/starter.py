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

    # TODO 1: add the fields role (str), content (str) and tags (list, empty by default)

    def word_count(self):
        # TODO 2: return how many words self.content has
        return None

    def to_dict(self):
        # TODO 3: return the message as a dict
        return None
