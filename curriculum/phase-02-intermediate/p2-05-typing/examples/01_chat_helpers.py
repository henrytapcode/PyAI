# Chat helpers: small typed functions that build and inspect a conversation.
def make_message(role: str, text: str) -> dict[str, str]:
    return {"role": role, "text": text}


def count_words(messages: list[dict[str, str]]) -> int:
    total = 0
    for message in messages:
        total += len(message["text"].split())
    return total


def last_from(messages: list[dict[str, str]], role: str) -> str | None:
    found = None
    for message in messages:
        if message["role"] == role:
            found = message["text"]
    return found


def summarize(messages: list[dict[str, str]]) -> tuple[int, int]:
    return len(messages), count_words(messages)


chat = [
    make_message("user", "What is a type hint?"),
    make_message("assistant", "A label that says what kind of value to expect."),
    make_message("user", "Does Python check it?"),
]

print(last_from(chat, "assistant"))
print(last_from(chat, "system"))
count, words = summarize(chat)
print("messages:", count, "words:", words)
