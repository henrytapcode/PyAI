class Model:
    """Base class for all models."""

    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("write generate in a subclass")

    def describe(self):
        return f"model: {self.name}"


class CannedModel(Model):
    """A model that answers with ready-made replies, in order, then starts over."""

    def __init__(self, name, replies):
        super().__init__(name)
        self.replies = replies
        self.position = 0

    def generate(self, prompt):
        reply = self.replies[self.position]
        self.position += 1
        if self.position == len(self.replies):
            self.position = 0
        return reply

    def describe(self):
        return super().describe() + f" ({len(self.replies)} replies)"
