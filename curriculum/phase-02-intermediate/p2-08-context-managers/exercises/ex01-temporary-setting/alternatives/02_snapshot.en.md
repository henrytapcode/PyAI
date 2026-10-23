# Save a copy of the whole dict

Instead of remembering one key, take a copy of the whole dict first (`dict(config)`) and, in `finally`, empty the dict and refill it from the copy:

- `dict(config)` makes the copy.
- `config.clear()` empties the original dict.
- `config.update(snapshot)` puts the saved items back.

 This handles a missing key without an `if`. The trade-off: it also undoes any other changes made to the dict inside the block, and it copies everything, which is slow for a big dict. Pick it when you want "put the dict back exactly as it was", and pick the one-key version when only that key should be restored.
