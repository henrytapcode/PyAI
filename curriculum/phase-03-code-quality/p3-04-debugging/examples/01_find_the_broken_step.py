# Find the broken step in a text pipeline by printing the value after every step.
import re


def lowercase(text):
    return text.lower()


def remove_punctuation(text):
    return re.sub(r"[^a-z ]", "", text)


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
    return re.sub(r"[^a-z0-9 -]", "", text)


steps = [lowercase, remove_punctuation, collapse_spaces]
run(steps, "Use  GPT-4, now!")
