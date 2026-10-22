# A tiny version of the project: average + grade for each student.
def average(scores):
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def letter_grade(avg):
    if avg >= 8.5:
        return "A"
    if avg >= 7:
        return "B"
    return "C or below"


students = [
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
]

for student in students:
    avg = average(student["scores"])
    print(f"{student['name']}: {avg:.2f} ({letter_grade(avg)})")
