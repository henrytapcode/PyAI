# Test a prompt builder at its edges: no documents, an exact fit, one word too many.
def count_tokens(text):
    return len(text.split())


def build_prompt(question, documents, max_tokens):
    """The question, then each document that still fits in max_tokens words."""
    parts = [question]
    used = count_tokens(question)
    for doc in documents:
        size = count_tokens(doc)
        if used + size > max_tokens:
            break
        parts.append(doc)
        used = used + size
    return "\n".join(parts)


failures = []


def check(name, actual, expected):
    if actual == expected:
        print("PASS", name)
    else:
        print("FAIL", name)
        print("  expected", expected)
        print("  got     ", actual)
        failures.append(name)


# Arrange: a question of 3 words and documents of 2 words each.
question = "what is RAG"
docs = ["first document", "second document"]

check("no documents gives just the question", build_prompt(question, [], 10), "what is RAG")
check("documents that fit are added", build_prompt(question, docs, 10), "what is RAG\nfirst document\nsecond document")
check("an exact fit is included", build_prompt(question, docs, 5), "what is RAG\nfirst document")
check("one word over is left out", build_prompt(question, docs, 4), "what is RAG")
check("limit smaller than the question keeps the question", build_prompt(question, docs, 1), "what is RAG")
check("empty question and no documents", build_prompt("", [], 10), "")

print(f"{6 - len(failures)} passed, {len(failures)} failed")
