# A tiny test runner: it finds the test_ functions, runs them and reports PASS or FAIL.
def clean_text(text):
    # Bug on purpose: this only fixes double spaces, not longer runs.
    return text.strip().lower().replace("  ", " ")


def test_lowercases_text():
    assert clean_text("Hello") == "hello"


def test_trims_both_ends():
    assert clean_text("  hi  ") == "hi"


def test_removes_extra_spaces():
    result = clean_text("a   b")
    assert result == "a b", f"got '{result}'"


passed = 0
failed = 0
for name, func in list(globals().items()):
    if name.startswith("test_") and callable(func):
        try:
            func()
            print("PASS", name)
            passed = passed + 1
        except AssertionError as error:
            print("FAIL", name, "-", error)
            failed = failed + 1

print(f"{passed} passed, {failed} failed")
