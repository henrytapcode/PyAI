# Prompt templates that remember their text and how often they were used.
class PromptTemplate:
    def __init__(self, name, template):
        self.name = name
        self.template = template
        self.uses = 0

    def fill(self, topic, audience):
        self.uses += 1
        text = self.template.replace("{topic}", topic)
        return text.replace("{audience}", audience)

    def __repr__(self):
        return f"PromptTemplate(name='{self.name}', uses={self.uses})"


explain = PromptTemplate("explain", "Explain {topic} to {audience} in two sentences.")
quiz = PromptTemplate("quiz", "Write a quiz question about {topic} for {audience}.")

print(explain.fill("classes", "a beginner"))
print(explain.fill("dicts", "a teacher"))
print(quiz.fill("loops", "a beginner"))
print(explain)
print(quiz)
