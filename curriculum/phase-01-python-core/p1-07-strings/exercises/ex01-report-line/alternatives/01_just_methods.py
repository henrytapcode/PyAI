def report_line(model, tokens, cost):
    left = model.ljust(12)
    middle = f"{tokens:,}".rjust(10)
    right = f"{cost:.2f}".rjust(8)
    return left + middle + right
