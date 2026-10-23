# Flatten messages from several chats and keep only the useful ones.
chats = [
    ["Hello", "", "How do I reset my password?"],
    ["  ", "Thanks!"],
    ["Show me an example of a list comprehension"],
]

all_messages = [msg for chat in chats for msg in chat]
print(len(all_messages))

useful = [msg.strip() for chat in chats for msg in chat if msg.strip()]
print(useful)

short = {msg: len(msg) for msg in useful if len(msg) <= 10}
print(short)
