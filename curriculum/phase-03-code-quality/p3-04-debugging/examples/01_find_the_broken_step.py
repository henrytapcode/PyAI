# Find the broken step in a text pipeline by printing the value after every step.

def lowercase(text):
    return text.lower()


def remove_punctuation(text):
    return "".join(ch for ch in text if ch.isalpha() or ch == " ")


def collapse_spaces(text):
    return " ".join(text.split())


def run(steps, value):
    for step in steps:
        value = step(value)
        print(step.__name__, "->", repr(value))
    return value


steps = [lowercase, remove_punctuation, collapse_spaces]
run(steps, "Use  GPT-4, now!")
print("---")


def remove_punctuation(text):
    return "".join(ch for ch in text if ch.isalnum() or ch in " -")


steps = [lowercase, remove_punctuation, collapse_spaces]
run(steps, "Use  GPT-4, now!")
