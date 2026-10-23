class TokenCounter:
    def __init__(self):
        self.total = 0
        self.calls = 0

    def add(self, n):
        self.total = self.total + n
        self.calls = self.calls + 1

    def average(self):
        return self.total / self.calls if self.calls else 0

    def __repr__(self):
        return f"TokenCounter(total={self.total}, calls={self.calls})"
