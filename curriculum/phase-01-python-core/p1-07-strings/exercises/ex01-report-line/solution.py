def report_line(model, tokens, cost):
    """Return one table row: model, tokens and cost, aligned in columns."""
    return f"{model:<12}{tokens:>10,}{cost:>8.2f}"
