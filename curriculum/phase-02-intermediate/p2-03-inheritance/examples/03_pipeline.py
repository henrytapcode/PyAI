# Composition: a Pipeline HAS a list of models and runs text through them.
class Model:
    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("write generate in a subclass")


class EchoModel(Model):
    def generate(self, prompt):
        return "echo: " + prompt


class ShoutModel(Model):
    def generate(self, prompt):
        return prompt.upper()


class TagModel(Model):
    def __init__(self, name, tag):
        super().__init__(name)
        self.tag = tag

    def generate(self, prompt):
        return f"<{self.tag}> {prompt}"


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def add(self, model):
        self.steps.append(model)

    def run(self, text):
        for step in self.steps:
            text = step.generate(text)
            print("after", step.name + ":", text)
        return text


pipe = Pipeline([EchoModel("echo-1"), ShoutModel("shout-1")])
pipe.add(TagModel("tag-1", "answer"))
result = pipe.run("hello")
print("final:", result)
print("steps:", len(pipe.steps))
print("is a Model:", isinstance(pipe, Model))
