# while, break and continue: add numbers until the total is big enough.
total = 0
number = 0
while True:
    number += 1
    if number % 2 == 0:
        continue          # skip even numbers
    total += number
    print(f"added {number}, total={total}")
    if total > 20:
        break             # stop the loop early
print("Stopped at", number)
