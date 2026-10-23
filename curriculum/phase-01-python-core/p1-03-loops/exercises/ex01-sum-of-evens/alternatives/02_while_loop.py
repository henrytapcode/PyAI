def sum_of_evens(n):
    """Return the sum of all even numbers from 1 to n (inclusive)."""
    total = 0
    number = 1
    while number <= n:
        if number % 2 == 0:
            total += number
        number += 1
    return total
