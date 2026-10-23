# A family of models: one base class, three subclasses, one loop.
class Model:
    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("write generate in a subclass")

    def describe(self):
        return f"model {self.name}"


class EchoModel(Model):
    def generate(self, prompt):
        return "echo: " + prompt


class CannedModel(Model):
    def __init__(self, name, reply):
        super().__init__(name)
        self.reply = reply

    def generate(self, prompt):
        return self.reply


class ChatModel(Model):
    def __init__(self, name, system):
        super().__init__(name)
        self.system = system

    def generate(self, prompt):
        return f"[{self.system}] {prompt}"


models = [
    EchoModel("echo-1"),
    CannedModel("canned-1", "I can only say this."),
    ChatModel("chat-1", "polite"),
]
for model in models:
    print(model.describe())
    print("  reply:", model.generate("What is Python?"))
    print("  is a Model:", isinstance(model, Model))
