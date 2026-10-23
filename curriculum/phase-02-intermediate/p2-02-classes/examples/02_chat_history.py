# A tiny chat history: ChatMessage objects stored in a list inside a ChatHistory object.
class ChatMessage:
    def __init__(self, role, text):
        self.role = role
        self.text = text

    def word_count(self):
        return len(self.text.split())

    def __repr__(self):
        return f"ChatMessage(role='{self.role}', words={self.word_count()})"


class ChatHistory:
    def __init__(self):
        self.messages = []

    def add(self, role, text):
        self.messages.append(ChatMessage(role, text))

    def total_words(self):
        total = 0
        for message in self.messages:
            total += message.word_count()
        return total

    def last_text(self, role):
        found = None
        for message in self.messages:
            if message.role == role:
                found = message.text
        return found


history = ChatHistory()
history.add("user", "What is a class?")
history.add("assistant", "A blueprint for making objects.")
history.add("user", "And an object?")

print(history.messages)
print("words:", history.total_words())
print("last user message:", history.last_text("user"))
print("last system message:", history.last_text("system"))
