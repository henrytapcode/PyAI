def report_line(model, tokens, cost):
    name_width = 12
    token_width = 10
    cost_width = 8
    return f"{model:<{name_width}}{tokens:>{token_width},}{cost:>{cost_width}.2f}"
