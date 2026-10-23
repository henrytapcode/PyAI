class Model:
    """Base class for all models.

    Example: Model("base").describe() returns "model: base"
    """

    def __init__(self, name):
        # TODO 1: store name in self.name
        pass

    def generate(self, prompt):
        # TODO 2: raise NotImplementedError("write generate in a subclass")
        return None

    def describe(self):
        # TODO 3: return "model: " followed by the name
        return None


class CannedModel(Model):
    """A model that answers with ready-made replies, in order, then starts over.

    Example: CannedModel("c1", ["Hi!", "Bye!"]).describe() returns "model: c1 (2 replies)"
    """

    def __init__(self, name, replies):
        # TODO 4: let the parent store the name (super().__init__)
        # TODO 5: keep replies in self.replies and start a call counter at 0
        pass

    def generate(self, prompt):
        # TODO 6: pick the reply at position (counter % number of replies)
        # TODO 7: add 1 to the counter, then return the reply
        return None

    def describe(self):
        # TODO 8: start from super().describe() and add " (N replies)"
        return None
