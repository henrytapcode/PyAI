class Message:
    def __init__(self, role, content, tags=None):
        self.role = role
        self.content = content
        if tags is None:
            tags = []
        self.tags = tags

    def word_count(self):
        return len(self.content.split())

    def to_dict(self):
        return {"role": self.role, "content": self.content, "tags": self.tags}

    def __repr__(self):
        return f"Message(role='{self.role}', content='{self.content}', tags={self.tags})"

    def __eq__(self, other):
        return (
            self.role == other.role
            and self.content == other.content
            and self.tags == other.tags
        )
