# Count how often each word appears: the seed of NLP.
words = ["ai", "is", "fun", "ai", "is", "everywhere", "ai"]

counts = {}
for word in words:
    if word in counts:
        counts[word] = counts[word] + 1
    else:
        counts[word] = 1

print(counts)
print(counts["ai"])
print(counts.get("python", 0))
for word, n in counts.items():
    print(f"{word}: {n}")
