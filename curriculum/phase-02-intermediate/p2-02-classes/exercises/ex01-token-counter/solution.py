class TokenCounter:
    """Track how many tokens a feature has used."""

    def __init__(self):
        self.total = 0
        self.calls = 0

    def add(self, n):
        self.total += n
        self.calls += 1

    def average(self):
        if self.calls == 0:
            return 0
        return self.total / self.calls

    def __repr__(self):
        return f"TokenCounter(total={self.total}, calls={self.calls})"
