class MessageLog:
    """Keep chat messages. This code has 3 bugs (all are a forgotten self).

    Example:
        log = MessageLog()
        log.add("hi")
        log.add("hello there")
        log.count()     # 2
        log.longest()   # "hello there"
    """

    def __init__(self):
        messages = []

    def add(text):
        self.messages.append(text)

    def count(self):
        return len(messages)

    def longest(self):
        best = ""
        for text in self.messages:
            if len(text) > len(best):
                best = text
        return best
