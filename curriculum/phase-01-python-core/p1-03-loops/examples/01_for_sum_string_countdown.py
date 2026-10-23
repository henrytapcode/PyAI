# for loops: range(), a string, and the accumulator pattern.
total = 0
for n in range(1, 6):
    total += n
    print(f"n={n} total={total}")
print("Sum of 1..5:", total)

for letter in "AI":
    print("letter:", letter)

for step in range(10, 0, -3):
    print("countdown:", step)
