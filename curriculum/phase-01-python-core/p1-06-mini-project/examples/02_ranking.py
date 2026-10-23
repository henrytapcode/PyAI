# Rank students: build small rows, sort them with a key helper, print a numbered list.
def average(scores):
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def sort_key(row):
    return (-row["avg"], row["name"])


students = [
    {"name": "Zoe", "scores": [7, 7]},
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Bao", "scores": [9, 9.5, 8.5]},
    {"name": "Mai", "scores": [7]},
]

rows = []
for student in students:
    rows.append({"name": student["name"], "avg": average(student["scores"])})

rank = 1
for row in sorted(rows, key=sort_key):
    print(f"{rank}. {row['name']} - {row['avg']:.2f}")
    rank += 1
