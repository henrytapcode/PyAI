class Model:
    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("subclasses must implement generate")


class ShoutModel(Model):
    def generate(self, text: str) -> str:
        return text.upper()


class EchoModel(Model):
    def generate(self, text: str) -> str:
        return f"echo: {text}"


class Pipeline:
    """Run text through a list of models, one after another.

    A Pipeline HAS models; it is not a Model.
    Example: Pipeline([ShoutModel("s"), EchoModel("e")]).run("hi") returns "echo: HI"
    """

    def __init__(self, steps):
        self.steps = steps

    def add(self, model):
        self.steps.append(model)

    def run(self, text):
        for step in self.steps:
            text = step.generate(text)
        return text

    def size(self):
        return len(self.steps)
