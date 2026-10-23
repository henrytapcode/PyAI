# A small class roster: a list of dicts, one dict per student.
students = [
    {"name": "Lan", "score": 9},
    {"name": "Minh", "score": 7},
    {"name": "Hoa"},
]

best_name = ""
best_score = 0
for student in students:
    score = student.get("score", 0)
    print(f"{student['name']}: {score}")
    if score > best_score:
        best_score = score
        best_name = student["name"]

print(f"Best: {best_name} ({best_score})")
pair = (best_name, best_score)
name, score = pair
print(name, score)
