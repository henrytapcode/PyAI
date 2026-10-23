# Count how many students got each letter, then draw a text histogram.
letters = ["B", "A", "B", "F", "B", "A", "C"]

counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for letter in letters:
    counts[letter] += 1

print(counts)
for letter, how_many in counts.items():
    print(f"{letter}: {'#' * how_many} ({how_many})")
