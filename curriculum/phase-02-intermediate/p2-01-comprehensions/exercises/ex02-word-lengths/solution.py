words = ["token", "prompt", "model", "ai"]

# word -> number of characters
lengths = {word: len(word) for word in words}

# keep only the entries whose length is at least 5
long_lengths = {word: n for word, n in lengths.items() if n >= 5}

print(lengths)
print(long_lengths)
