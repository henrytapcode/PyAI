# A list of model scores: indexing, slicing, appending and looping.
scores = [0.82, 0.91, 0.78]
scores.append(0.95)

print(len(scores))
print(scores[0], scores[-1])
print(scores[1:3])

total = 0
for s in scores:
    total = total + s
average = total / len(scores)
print(f"Average: {round(average, 3)}")
print(sorted(scores))
print(0.91 in scores)
