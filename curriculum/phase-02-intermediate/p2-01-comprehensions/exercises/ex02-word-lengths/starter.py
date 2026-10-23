words = ["token", "prompt", "model", "ai"]

# word -> number of characters
lengths = {word: ___(word) for word in words}

# keep only the entries whose length is at least 5
long_lengths = {word: n for word, n in lengths.___() if n >= ___}

print(lengths)
print(long_lengths)
