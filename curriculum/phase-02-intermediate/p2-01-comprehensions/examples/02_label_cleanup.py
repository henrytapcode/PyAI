# Clean messy labels, remove duplicates, then count them.
raw_labels = ["Positive", " negative", "POSITIVE ", "neutral", "Negative", "positive"]

cleaned = [label.strip().lower() for label in raw_labels]
print(cleaned)

unique_labels = sorted({label for label in cleaned})
print(unique_labels)

counts = {name: len([x for x in cleaned if x == name]) for name in unique_labels}
print(counts)

flags = ["ok" if counts[name] >= 2 else "rare" for name in unique_labels]
print(flags)
