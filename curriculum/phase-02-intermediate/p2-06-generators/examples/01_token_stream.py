# Stream a reply token by token, the way a chatbot shows its answer.
def stream_reply(text):
    for token in text.split():
        yield token + " "


reply = "Generators produce one token at a time"
stream = stream_reply(reply)

first = next(stream)
print("first token:", first.strip())

for token in stream:
    print("got:", token.strip())

full = "".join(stream_reply(reply)).strip()
print(full)
print(len(full.split()), "tokens")
