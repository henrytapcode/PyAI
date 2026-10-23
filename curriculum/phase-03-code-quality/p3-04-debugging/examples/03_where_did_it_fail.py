# Catch an error and report its type, its message, and the chain of function calls.
import traceback


def parse_score(text):
    return int(text)


def load_scores(lines):
    scores = []
    for line in lines:
        scores.append(parse_score(line))
    return scores


def main():
    try:
        load_scores(["10", "abc", "7"])
    except ValueError as err:
        frames = traceback.extract_tb(err.__traceback__)
        print("error:", type(err).__name__, "-", err)
        print("path:", " -> ".join(frame.name for frame in frames))
        print("frames:", len(frames))


main()
