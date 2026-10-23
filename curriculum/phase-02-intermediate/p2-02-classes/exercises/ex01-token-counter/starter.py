class TokenCounter:
    """Track how many tokens a feature has used.

    Example:
        counter = TokenCounter()
        counter.add(10)
        counter.add(20)
        counter.total       # 30
        counter.calls       # 2
        counter.average()   # 15.0
        print(counter)      # TokenCounter(total=30, calls=2)
    """

    def __init__(self):
        # TODO 1: create self.total and self.calls, both starting at 0
        pass

    def add(self, n):
        # TODO 2: add n to self.total and add 1 to self.calls
        pass

    def average(self):
        # TODO 3: if self.calls is 0, return 0
        # TODO 4: otherwise return self.total divided by self.calls
        return None

    def __repr__(self):
        # TODO 5: return (do not print) the text TokenCounter(total=30, calls=2)
        #         using the real numbers; an f-string works well here
        return ""
