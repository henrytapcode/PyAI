# Check a score parser with a table of cases, the way parametrize does.
def parse_score(text):
    parts = text.split("/")
    if len(parts) != 2:
        raise ValueError(f"expected 'a/b', got {text}")
    return int(parts[0]) / int(parts[1])


def error_name(text):
    try:
        parse_score(text)
    except ValueError:
        return "ValueError"
    except ZeroDivisionError:
        return "ZeroDivisionError"
    return "no error"


VALID = [("8/10", 0.8), ("0/5", 0.0), ("5/5", 1.0), ("1/3", 0.3333)]
INVALID = ["abc", "8", "1/2/3", "x/10", "8/0"]

bad = 0
for text, expected in VALID:
    result = parse_score(text)
    if abs(result - expected) < 1e-3:
        print(f"PASS {text} -> {expected}")
    else:
        print(f"FAIL {text}: expected {expected}, got {result}")
        bad = bad + 1

for text in INVALID:
    name = error_name(text)
    if name == "ValueError":
        print(f"PASS {text} raises ValueError")
    else:
        print(f"FAIL {text}: expected ValueError, got {name}")
        bad = bad + 1

print(f"{len(VALID) + len(INVALID) - bad} ok, {bad} failed")
