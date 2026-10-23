When you test a prompt, you often want to change one setting for a single block of code, such as a higher `temperature`, and then get the old setting back, even if the block fails. Write the context manager `temporary_setting(config, key, value)`. Inside the `with` block, `config[key]` equals `value`. When the block ends, the setting goes back to what it was before. Write your code inside the function, for example with `@contextmanager` and `yield`.

**Example**

```python
config = {"model": "small"}
with temporary_setting(config, "model", "big"):
    print(config["model"])   # big
print(config["model"])       # small
```

**Rules**
- Change the dict you receive in place (the caller must see the new value).
- If `key` was already in `config`, restore its old value afterwards.
- If `key` was **not** in `config`, remove it afterwards, so the dict looks the same as before.
- The restore also happens when the block raises an error, and that error must still reach the caller (do not hide it).
- Managers can be nested: restoring must bring back exactly the value that was there when this manager started.
