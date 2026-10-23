# Skip bad records with a manager that hides only one kind of error.
class SkipErrors:
    def __init__(self, error_type):
        self.error_type = error_type
        self.skipped = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(exc_value, self.error_type):
            self.skipped += 1
            return True
        return False


raw_scores = ["0.9", "n/a", "0.7", "", "0.8"]
scores = []
skip = SkipErrors(ValueError)

for text in raw_scores:
    with skip:
        scores.append(float(text))

print(scores)
print("skipped:", skip.skipped)

try:
    with skip:
        scores.append(float(None))
except TypeError:
    print("TypeError was not hidden")

print("skipped:", skip.skipped)
