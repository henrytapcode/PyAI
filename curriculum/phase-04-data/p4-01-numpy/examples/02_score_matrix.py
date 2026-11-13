# Summarise a 2D student score matrix by quiz (axis=0) and by student (axis=1).
import numpy as np

students = ["An", "Binh", "Chi", "Dung"]
scores = np.array([
    [8.0, 7.5, 9.0],
    [6.5, 8.0, 7.0],
    [9.0, 9.5, 8.5],
    [7.0, 6.0, 8.0],
])

quiz_means = np.round(scores.mean(axis=0), 2)
student_means = np.round(scores.mean(axis=1), 2)
print("quiz means:", quiz_means)
print("student means:", student_means)

top_index = int(student_means.argmax())
print("top student:", students[top_index], "with", float(student_means[top_index]))
