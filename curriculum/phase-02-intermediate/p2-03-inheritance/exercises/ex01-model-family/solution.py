class Model:
    """Base class for all models.

    Example: Model("base").describe() returns "model: base"
    """

    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("write generate in a subclass")

    def describe(self):
        return f"model: {self.name}"


class CannedModel(Model):
    """A model that answers with ready-made replies, in order, then starts over.

    Example: CannedModel("c1", ["Hi!", "Bye!"]).describe() returns "model: c1 (2 replies)"
    """

    def __init__(self, name, replies):
        super().__init__(name)
        self.replies = replies
        self.calls = 0

    def generate(self, prompt):
        reply = self.replies[self.calls % len(self.replies)]
        self.calls += 1
        return reply

    def describe(self):
        return super().describe() + f" ({len(self.replies)} replies)"
