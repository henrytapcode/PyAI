# Run a table of (input, expected) cases the way parametrize does, and report which ones fail.
def normalize_spaces(text):
    return " ".join(text.split())


cases = [
    ("  a   b ", "a b"),
    ("a\n\tb", "a b"),
    ("", ""),
    ("   ", ""),
    ("one", "one "),  # a wrong expectation: the test, not the function, is broken
]

passed = 0
failed = []
for text, expected in cases:
    result = normalize_spaces(text)
    if result == expected:
        passed += 1
    else:
        failed.append((text, expected, result))

for text, expected, result in failed:
    print("FAIL", repr(text), "expected", repr(expected), "got", repr(result))
print(passed, "passed,", len(failed), "failed")
