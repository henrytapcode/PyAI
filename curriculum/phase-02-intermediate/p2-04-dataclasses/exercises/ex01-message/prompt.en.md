Turn `Message` into a dataclass for a chat app. A message has a role, a text and a list of tags, and it can count its words and turn itself into a dict. Write your code inside the class and the two methods, and `return` the answers (do not print them).

**Example**

```python
msg = Message("user", "Hi there")
print(msg)                # Message(role='user', content='Hi there', tags=[])
print(msg.word_count())   # 2
print(msg.to_dict())      # {'role': 'user', 'content': 'Hi there', 'tags': []}
print(msg == Message("user", "Hi there"))   # True
```

**Rules**
- `Message` has three fields in this order: `role`, `content` and `tags`.
- `role` and `content` are required. `tags` is optional and is an empty list by default.
- Every message has its **own** `tags` list: adding a tag to one message must not change another.
- `word_count()` returns how many words `content` has (words are separated by spaces). An empty `content` has `0` words.
- `to_dict()` returns a dict with the keys `"role"`, `"content"` and `"tags"`.
