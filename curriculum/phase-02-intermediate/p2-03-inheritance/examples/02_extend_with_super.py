# Extend a parent method with super(): a model that counts its calls.
class Model:
    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        return "echo: " + prompt

    def describe(self):
        return f"model {self.name}"


class CountingModel(Model):
    def __init__(self, name):
        super().__init__(name)
        self.calls = 0

    def generate(self, prompt):
        self.calls += 1
        return super().generate(prompt)

    def describe(self):
        return super().describe() + f", calls so far: {self.calls}"


bot = CountingModel("counter-1")
print(bot.describe())
for question in ["a", "b", "c"]:
    print(bot.generate(question))
print(bot.describe())
