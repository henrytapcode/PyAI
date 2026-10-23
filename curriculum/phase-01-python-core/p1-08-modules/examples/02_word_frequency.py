# Count word frequencies with collections.Counter.
from collections import Counter

text = "the cat sat on the mat the dog sat on the log"
words = text.split()

counts = Counter(words)

print(counts)
print(counts["the"])
print(counts["bird"])
print(counts.most_common(2))

for word, number in counts.most_common(3):
    print(f"{word:<4} {number}")
