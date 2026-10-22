def sum_of_evens(n):
    """Return the sum of all even numbers from 1 to n (inclusive)."""
    total = 0
    for number in range(1, n + 1):
        if number % 2 == 0:
            total += number
    return total
