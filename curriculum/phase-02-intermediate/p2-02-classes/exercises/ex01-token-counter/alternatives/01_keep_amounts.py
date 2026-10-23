class TokenCounter:
    def __init__(self):
        self.amounts = []
        self.total = 0
        self.calls = 0

    def add(self, n):
        self.amounts.append(n)
        self.total = sum(self.amounts)
        self.calls = len(self.amounts)

    def average(self):
        if len(self.amounts) == 0:
            return 0
        return sum(self.amounts) / len(self.amounts)

    def __repr__(self):
        return "TokenCounter(total=" + str(self.total) + ", calls=" + str(self.calls) + ")"
