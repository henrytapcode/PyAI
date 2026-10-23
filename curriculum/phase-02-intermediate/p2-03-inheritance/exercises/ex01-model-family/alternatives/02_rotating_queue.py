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
        self.queue = list(replies)

    def generate(self, prompt):
        reply = self.queue.pop(0)
        self.queue.append(reply)
        return reply

    def describe(self):
        return super().describe() + f" ({len(self.replies)} replies)"
