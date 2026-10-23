# Token budgets: each feature gets its own TokenCounter object with its own limit.
class TokenCounter:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.total = 0

    def add(self, n):
        self.total += n

    def remaining(self):
        return self.limit - self.total

    def __repr__(self):
        return f"TokenCounter(name='{self.name}', total={self.total}/{self.limit})"


chat = TokenCounter("chat", 1000)
search = TokenCounter("search", 200)

for used in [120, 300, 450]:
    chat.add(used)
for used in [90, 130]:
    search.add(used)

print(chat)
print(search)
for counter in [chat, search]:
    if counter.remaining() < 0:
        print(counter.name, "is over budget by", -counter.remaining())
    else:
        print(counter.name, "has", counter.remaining(), "tokens left")
