class MessageLog:
    """Keep chat messages."""

    def __init__(self):
        self.messages = []

    def add(self, text):
        self.messages.append(text)

    def count(self):
        return len(self.messages)

    def longest(self):
        best = ""
        for text in self.messages:
            if len(text) > len(best):
                best = text
        return best
